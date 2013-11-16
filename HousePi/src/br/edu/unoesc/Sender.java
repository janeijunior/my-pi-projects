package br.edu.unoesc;


import java.io.DataOutputStream;
import java.io.IOException;
import android.os.Handler;
import android.os.Message;

/**
 * 
 * @author Rodrigo
 * 
 */
class Sender implements Runnable {

	private DataOutputStream out;
	private boolean running = true;
	private Handler handler;
	private Message msg;
	private String sendMessage;

	public Sender(DataOutputStream out, Handler handler) {
		this.out = out;
		this.handler = handler;
	}

	@Override
	public void run() {
		while (running) {// Enquanto estiver executando

			try {
				if (sendMessage != null) { // Se existir uma mensagem para
											// enviar
					msg = new Message();
					msg.arg1 = ConnectionSocket.SENDING_MESSAGE;
					handler.sendMessage(msg); // Notifica Handler

					out.writeUTF(sendMessage); // Escreve mensagem
					out.flush();
					sendMessage = null; // Seta nulo na mensagem
				}

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
			out.close();
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
		out.close();
	}

}
