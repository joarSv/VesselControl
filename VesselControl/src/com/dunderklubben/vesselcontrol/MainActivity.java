package com.dunderklubben.vesselcontrol;

import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Bundle;
import android.os.PowerManager;
import android.preference.PreferenceManager;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.SharedPreferences.OnSharedPreferenceChangeListener;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class MainActivity extends Activity implements SensorEventListener  {
	PowerManager.WakeLock wakeLock;
	SharedPreferences sharedPrefs;
	
	private boolean paused;
	private byte lastX, lastY;
	
	//Controls
	private EditText txtIp;
	private Button btnConnect;
	private VesselClient client;
	private SensorManager sensorManager;
	private TextView lblNotification;
	
	//Settings
	private boolean stay_awake;
	private int threshold;
	
	private OnSharedPreferenceChangeListener settingsListener = new SharedPreferences.OnSharedPreferenceChangeListener() {
		  public void onSharedPreferenceChanged(SharedPreferences prefs, String key) {
			  Log.d("SKIP", "Setting changed: " + key);
			  if(key.equalsIgnoreCase("stay_awake")) {
					stay_awake = prefs.getBoolean("stay_awake", true);
					if(stay_awake)
						wakeLock.acquire();
					else
						wakeLock.release();
				}		
				else if(key.equalsIgnoreCase("threshold")) {
			        threshold = Integer.parseInt(sharedPrefs.getString("threshold", "5"));
				}
		  }
	};

	
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);        
        setContentView(R.layout.activity_main);
        
        //Get system services
        sharedPrefs = PreferenceManager.getDefaultSharedPreferences(this);
        sharedPrefs.registerOnSharedPreferenceChangeListener(settingsListener);
        PowerManager pm = (PowerManager) getSystemService(Context.POWER_SERVICE); 
        sensorManager = (SensorManager)getSystemService(SENSOR_SERVICE);              
        wakeLock = pm.newWakeLock(PowerManager.FULL_WAKE_LOCK, "VesselControl");
        
        //Get preferences
        stay_awake = sharedPrefs.getBoolean("stay_awake", true);	
        threshold = Integer.parseInt(sharedPrefs.getString("threshold", "5"));
        
        //Get controls
        lblNotification = (TextView)findViewById(R.id.lblNotification);
        btnConnect = (Button)findViewById(R.id.btnConnect);
        txtIp = (EditText)findViewById(R.id.txtIp);        
        
        //Init misc values
        client = new VesselClient();
        lastX = 0; 
        lastY = 0;
        paused = false;
        
        if(stay_awake)
        	wakeLock.acquire();
    }
    
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.activity_main, menu);
        return true;
    }
    
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {    
    	switch (item.getItemId()) {   
			case R.id.menu_settings:   
				startActivity(new Intent(this, SettingsActivity.class));    
				return true;    
		}
		return false;
    }
    
    @Override
    public void onPause() {
    	super.onPause();
    	if(client.isConnected()) {
    		client.close();
    		sensorManager.unregisterListener(this);
    		paused = true;
    	}	
    	if(stay_awake)
    		wakeLock.release();
    }
    
    @Override
    public void onResume() {
    	super.onResume();
    	if(stay_awake)
    		wakeLock.acquire();
    	
    	if(paused) {
    		connect(null);
    		paused = false;
    	}
    }
    
    @Override
    public void onDestroy() {
    	super.onDestroy();
    	if(stay_awake)
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
			
			if(byteX < lastX-threshold || byteX > lastX+threshold) {
				client.send(bX);
				lastX = byteX; 
			}
			if(byteY < lastY-threshold || byteY > lastY+threshold ) {
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
