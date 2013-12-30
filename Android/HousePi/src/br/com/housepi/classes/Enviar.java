package br.com.housepi.classes;


import java.io.DataOutputStream;
import java.io.IOException;
import android.os.Handler;
import android.os.Message;

/**
 * 
 * @author Rodrigo
 * 
 */

class Enviar implements Runnable {

	private DataOutputStream out;
	private boolean running = true;
	private Handler handler;
	private Message msg;
	private String mensagem;

	public Enviar(DataOutputStream out, Handler handler) {
		this.out = out;
		this.handler = handler;
	}

	@Override
	public void run() {
		while (running) {

			try {
				if (mensagem != null) { 
					out.writeUTF(mensagem); 
					out.flush();
					mensagem = null; 
				}

			} catch (IOException e) {
				e.printStackTrace();
				msg = new Message();
				msg.arg1 = -1;
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

	public void setMensagem(String mensagem) {
		this.mensagem = mensagem;

	}

	public void disconnect() throws Exception {
		running = false;
		out.close();
	}

}
