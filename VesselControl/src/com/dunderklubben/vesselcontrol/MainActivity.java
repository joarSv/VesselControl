package com.dunderklubben.vesselcontrol;

import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.os.PowerManager;
import android.app.Activity;
import android.content.Context;
import android.view.Menu;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class MainActivity extends Activity implements SensorEventListener {
	private byte lastX, lastY;
	private final byte THRESHOLD = 5;
	PowerManager.WakeLock wakeLock;
	private boolean paused;
	
	private EditText txtIp;
	private Button btnConnect;
	private LabClient client;
	private SensorManager sensorManager;
	private TextView lblNotification;
	
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        PowerManager pm = (PowerManager) getSystemService(Context.POWER_SERVICE);
        wakeLock = pm.newWakeLock(PowerManager.FULL_WAKE_LOCK, "VesselControl");
        wakeLock.acquire();

        sensorManager = (SensorManager)getSystemService(SENSOR_SERVICE);        
        
        lblNotification = (TextView)findViewById(R.id.lblNotification);
        btnConnect = (Button)findViewById(R.id.btnConnect);
        txtIp = (EditText)findViewById(R.id.txtIp);
        client = new LabClient();
        lastX = 0; 
        lastY = 0;
        paused = false;
    }
    
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.activity_main, menu);
        return true;
    }
    
    @Override
    public void onPause() {
    	super.onPause();
    	if(client.isConnected()) {
    		client.close();
    		sensorManager.unregisterListener(this);
    		paused = true;
    	}	
    	wakeLock.release();
    }
    
    @Override
    public void onResume() {
    	super.onResume();
    	wakeLock.acquire();
    	if(paused) {
    		connect(null);
    		paused = false;
    	}
    }
    
    @Override
    public void onDestroy() {
    	super.onDestroy();
    	wakeLock.release();
    	if(client.isConnected()) {
    		client.close();
    		sensorManager.unregisterListener(this);
    	}	
    }
    
    public void connect(View v) {
    	if(!client.isConnected()) {
    		if(client.connect(txtIp.getText().toString())) {
    			btnConnect.setText("Disconnect");
    			lblNotification.setText("");
    			sensorManager.registerListener(this, sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER), SensorManager.SENSOR_DELAY_GAME);
    		} else {
    			lblNotification.setText("Could not connect to the server");
    		}
    	} else {
    		client.close();
    		sensorManager.unregisterListener(this);
    		btnConnect.setText("Connect");
    	}
    }

	public void onAccuracyChanged(Sensor sensor, int accuracy) {		
	}
	public void onSensorChanged(SensorEvent event) {
		if(client.isConnected()) {
			float x = event.values[0], y = event.values[1];
			byte byteX = map(x), byteY = map(y);
			byte bX[] = {(byte)((int)1), byteX}, bY[] = {(byte)((int)2), byteY};
			
			if(byteX < lastX-THRESHOLD || byteX > lastX+THRESHOLD) {
				client.send(bX);
				lastX = byteX; 
			}
			if(byteY < lastY-THRESHOLD || byteY > lastY+THRESHOLD ) {
				client.send(bY);
				lastY = byteY;
			}
		}
		else
			sensorManager.unregisterListener(this);
	}

	public byte map(float value) {
		float fMAX = 7, fMIN = -7;
		int bMAX = 180, bMIN = 0;
		value = Math.max(fMIN,Math.min(fMAX, value));
		
		int result = (int)((value - fMIN) * (bMAX - bMIN) / (fMAX - fMIN) + bMIN);
		
		return (byte)result;
	}
}
