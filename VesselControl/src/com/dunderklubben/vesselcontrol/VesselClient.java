package com.dunderklubben.vesselcontrol;

import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import android.os.AsyncTask;

public class LabClient {
	private boolean _connected;
	private Socket _client;
	
	public LabClient () {
		_connected = false;
		_client = new Socket();
	}
	
	public boolean connect(String ip, int port) {
		ConnectTask task = new ConnectTask(_client);
		task.execute(ip, "" + port);
		try {
			boolean ret = task.get();
			if(!ret) //Socket is closed and will not be able to connect... recreate the socket.
				_client = new Socket();
			
			return ret;
		} catch (Exception e) {
			e.printStackTrace();
			return false;
		}
	}	
	public boolean connect(String ip){
		return connect(ip, 1000);
	}
	
	public void close() {
		try {
			this._client.close();
		} catch (IOException e) {			
			e.printStackTrace();
			
		}
		this._client = new Socket(); //Closed socket cannot connect. To be able to connect once again, the socket is re-created.
		_connected = false;
	}
	
	public void send(String data) {
		if(_connected) {
			try {
				PrintWriter writer = new PrintWriter(_client.getOutputStream());
				writer.println(data);
				writer.flush();
			} catch (IOException e) {
				e.printStackTrace();
				_connected = false;
			}
		}		
	}
	public void send(byte[] data) {
		if(_connected) {
			try {
				OutputStream os = _client.getOutputStream();
				os.write(data);
				os.flush();
			} catch (IOException e) {
				e.printStackTrace();
				_connected = false;
			}
		}
	}

	public boolean isConnected() {
		return this._connected;
	}
	
	private class ConnectTask extends AsyncTask<String, Void, Boolean> {
		Socket client;
		
		public ConnectTask(Socket client) {
			this.client = client;
		}
		
		@Override
		protected void onPostExecute(Boolean result){
			_connected = result;
		}
		
		@Override
		protected Boolean doInBackground(String... params) {
			String ip = params[0];
			int port = Integer.parseInt(params[1]);
			try {
				if(!_connected) {
					client.connect(new InetSocketAddress(ip, port));
					_connected = true;
				}				
			} catch (UnknownHostException e) {
				e.printStackTrace();
				return false;
			} catch (IOException e) {
				e.printStackTrace();
				return false;
			}			
			return true;
		}		
	}
}
