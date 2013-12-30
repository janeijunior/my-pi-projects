package br.com.housepi.classes;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.Socket;

import android.os.Handler;

/**
 *@author Rodrigo
 * 
 */

public class Conexao {

	private static Conexao conexao;
	private int porta;
	private String host;
	private  Socket socket;
	private Enviar enviar;
	private DataOutputStream out;
	private DataInputStream in;

	public DataInputStream getIn() {
		return in;
	}

	private Conexao(String host, String porta) {
		this.host = host;
		this.porta = Integer.parseInt(porta);
	}

	public static Conexao createConnection(String host, String porta) {
		conexao = new Conexao(host, porta);
		return conexao;
	}

	public static Conexao getConexaoAtual() {
		return conexao;
	}

	public void conectar() throws Exception {
		this.socket = new Socket(host, porta);
		out = new DataOutputStream(socket.getOutputStream());
		in = new DataInputStream(socket.getInputStream());
		socket.setSoTimeout(10000);
	}

	public void iniciar(Handler handler) {
		enviar = new Enviar(out, handler);
		
		new Thread(enviar).start();
	}

	public void enviarMensagem(String mensagem) {
		enviar.setMensagem(mensagem);
	}

	public void disconnect() throws Exception {
		enviar.disconnect();
		socket.close();
	}
}
