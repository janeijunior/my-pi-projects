package br.edu.unoesc;

import java.io.DataInputStream;
import java.io.IOException;
import android.os.Handler;
import android.os.Message;

/**
 * 
 * @author Rodrigo
 * 
 */
class Receiver implements Runnable {

	private DataInputStream in;
	private boolean running = true;
	private Handler handler;
	private Message msg;
	private String sendMessage;

	public Receiver(DataInputStream in, Handler handler) {
		this.in = in;
		this.handler = handler;
	}

	@Override
	public void run() {
		while (running) {// Enquanto estiver executando

			try {
				sendMessage = in.readUTF();
				msg = new Message();
				msg.arg1 = ConnectionSocket.RECEIVED_MESSAGE;
				msg.obj = sendMessage;
				handler.sendMessage(msg);

			} catch (IOException e) {
				e.printStackTrace();
				msg = new Message();
				msg.arg1 = ConnectionSocket.ERROR;
				msg.obj = e.getMessage();
				handler.sendMessage(msg);
				running = false;
			}

		}
		try {
			in.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public boolean isRunning() {
		return running;
	}

	public void setRunning(boolean running) {
		this.running = running;
	}

	public void stop() {
		running = false;
	}

	public void setMessage(String message) {
		this.sendMessage = message;

	}

	public void disconnect() throws Exception {
		msg = new Message();
		msg.arg1 = ConnectionSocket.DISCONNECTED;
		handler.sendMessage(msg); // Notifica Handler
		running = false;
		in.close();
	}

}
