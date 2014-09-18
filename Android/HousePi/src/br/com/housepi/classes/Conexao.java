package br.com.housepi.classes;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.Socket;
import android.util.Log;
import br.com.housepi.activity.Login;


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
		InetSocketAddress inet = new InetSocketAddress(host, porta);
		String hostConexao = inet.getAddress().getHostAddress();
		
		this.socket = new Socket(hostConexao, porta);
		this.socket.setSoTimeout(15000);
		
		out = new DataOutputStream(socket.getOutputStream());
		in = new DataInputStream(socket.getInputStream());
	}

	public void iniciar() {
		enviar = new Enviar(out);
		new Thread(enviar).start();
	}

	public void enviarMensagem(String mensagem) {
		if (enviar != null) {
			enviar.setMensagem(mensagem);
		} else {
			new Thread() {
				public void run() {
					try{
						conexao = Conexao.createConnection(Login.IP_SERVIDOR, Login.PORTA_SERVIDOR);	
		    			conexao.conectar();
		    			conexao.iniciar();
		            } catch (Exception e) {
		            	Log.e("tag", e.getMessage());
		            }
				}
			}.start();
		}
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
		enviar = null;
		socket.close();
	}
}
