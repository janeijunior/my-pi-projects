package br.edu.unoesc;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.Socket;

import android.os.Handler;
import android.os.Message;

/**
 * 
 * @author Rodrigo
 * 
 */
public class ConnectionSocket {

	private static ConnectionSocket connection;
	private int porta;
	private String host;
	private Socket socket;
	private Sender sender;
	public static final int CONNECTED = 1;
	public static final int ERROR = 2;
	public static final int SENDING_MESSAGE = 3;
	public static final int DISCONNECTED = 4;
	public static final int RECEIVED_MESSAGE = 0;
	private Message msg;
	private DataOutputStream out;
	private Handler handler; // Handle para notificações na tela
	private DataInputStream in;
	private Receiver receiver;

	private ConnectionSocket(String host, String porta) {
		this.host = host;
		this.porta = Integer.parseInt(porta);
	}

	// Método que cria Objecto ConnectionSocket
	public static ConnectionSocket createConnection(String host, String porta) {
		connection = new ConnectionSocket(host, porta);
		return connection;
	}

	// Retorna conexão atual
	public static ConnectionSocket getCurentConnection() {
		return connection;
	}

	// Conecta com o Servidor
	public void connect() throws Exception {
		this.socket = new Socket(host, porta);
		out = new DataOutputStream(socket.getOutputStream());
		in = new DataInputStream(socket.getInputStream());
	}

	// Inicia Thread para envio de mensagens
	public void startSender(Handler handler) {
		sender = new Sender(out, handler);
		receiver = new Receiver(in, handler);
		new Thread(sender).start();
		new Thread(receiver).start();
		this.handler = handler;
	}

	// Método set mensagem para envio
	public void senMessage(String mensagem) {
		sender.setMessage(mensagem);
	}

	// Método para disconectar do Servidor
	public void disconnect() throws Exception {
		sender.disconnect();
		socket.close();
		if (handler != null) {
			msg = new Message();
			msg.arg1 = ConnectionSocket.DISCONNECTED;
			handler.sendMessage(msg);
		}

	}
}
