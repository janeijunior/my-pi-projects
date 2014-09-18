package br.com.housepi.classes;

import java.io.DataOutputStream;
import java.io.IOException;

/**
 * 
 * @author Rodrigo
 * 
 */

class Enviar implements Runnable {

	private DataOutputStream out;
	private boolean running = true;
	private String mensagem;

	public Enviar(DataOutputStream out) {
		this.out = out;
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
				
				try {
					Thread.sleep(100);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
			} catch (IOException e) {
				e.printStackTrace();
				mensagem = null;
				running = false;
				
				try {
					Conexao.getConexaoAtual().disconnect();
				} catch (Exception e1) {
					e1.printStackTrace();
				}
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
