package br.com.housepi.classes;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;

/**
 *@author Rodrigo
 * 
 */

public class Conexao {

	private static Conexao conexao;
	private static DataInputStream in;
	private int porta;
	private String host;
	private Socket socket;
	private Enviar enviar;
	private DataOutputStream out;

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
		socket.setSoTimeout(20000);
	}

	public void iniciar() {
		enviar = new Enviar(out);
		new Thread(enviar).start();
	}

	public void enviarMensagem(String mensagem) {
		enviar.setMensagem(mensagem);
	}
	
	@SuppressWarnings("deprecation")
	public static String receberRetornoStatic() {
		try {
			return in.readLine();
		} catch (IOException e) {
			e.printStackTrace();
			return "Erro";					
		}
	}
	
	public String receberRetorno() {
		return receberRetornoStatic();
	}

	public void disconnect() throws Exception {
		enviar.disconnect();
		socket.close();
	}
}
