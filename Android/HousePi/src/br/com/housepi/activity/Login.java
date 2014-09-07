package br.com.housepi.activity;
import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.output.XMLOutputter;

import br.com.housepi.R;
import br.com.housepi.classes.Conexao;
import br.com.housepi.classes.Funcoes;
//import android.net.wifi.WifiInfo;
//import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.support.v4.view.MenuItemCompat;
import android.support.v7.app.ActionBarActivity;
import android.text.InputType;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.CheckBox;
import android.widget.EditText;

@SuppressLint("NewApi")
public class Login extends ActionBarActivity {
	private static final int MENU_CONFIG = 1;
	private static final int ERRO_CONEXAO = -1;
	private Context context = this; 
	private String msgErro;
	private EditText edtUsuario;
	private EditText edtSenha;
	private CheckBox cbxMostrarSenha;
	private CheckBox cbxSalvarSenha;
	
	public static String IP_SERVIDOR;
	public static String PORTA_SERVIDOR;
	public static String USUARIO;
	public static String SENHA;
	
	private ProgressDialog dialog;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.login);
		
		edtUsuario = (EditText) findViewById(R.id.edtUsuario);
		edtSenha = (EditText) findViewById(R.id.edtSenha);
		
		cbxMostrarSenha = (CheckBox) findViewById(R.id.cbxMostrarSenha);
		cbxSalvarSenha = (CheckBox) findViewById(R.id.cbxSalvarSenha);
		
		carregarComponentes();
	}
	
	private void carregarComponentes() {
		edtUsuario.setText(Funcoes.carregarDadosComponente("edtUsuario", edtUsuario.getText().toString(), this));
		edtSenha.setText(Funcoes.carregarDadosComponente("edtSenha", edtSenha.getText().toString(), this));
		cbxSalvarSenha.setChecked(Funcoes.carregarDadosComponente("cbxSalvarSenha", "1", this).equals("1"));
		
		if (cbxMostrarSenha.isChecked()) {
			edtSenha.setInputType(InputType.TYPE_CLASS_TEXT);
		} else {
			edtSenha.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD);	
		}
	}
	
	@Override
	protected void onPostResume() {
		carregarComponentes();		
		super.onPostResume();
	}

	@SuppressLint("HandlerLeak")
	private Handler handler = new Handler() {
		public void handleMessage(android.os.Message msg) {
			synchronized (msg) {
				switch (msg.arg1) {
				case ERRO_CONEXAO:
					dialog.dismiss();  
					AlertDialog.Builder builder = new AlertDialog.Builder(context);  
					builder.setMessage(msgErro);  
					builder.setCancelable(false);  
					builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {  
	                @Override  
	                public void onClick(DialogInterface dialog, int which) {  
	                    dialog.dismiss();  
	                	}  
					});  
	                
					AlertDialog alert = builder.create();  
					alert.show(); 
					break;
				}
			}
		};

	};

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		MenuItem item;
        
        item = menu.add(0, MENU_CONFIG, 0, "Configura��es");
		
		if (android.os.Build.VERSION.SDK_INT >= 11) { 
	        item.setShowAsActionFlags(MenuItemCompat.SHOW_AS_ACTION_ALWAYS | MenuItemCompat.SHOW_AS_ACTION_WITH_TEXT);
	        item.setIcon(R.drawable.ic_action_settings);
		}
		
		return true;
	}

	public void onClickConectar(View view) {
		if ((edtUsuario.getText().toString().trim().equals("")) || (edtSenha.getText().toString().trim().equals(""))) {
			Funcoes.msgDialogoInformacao("Aten��o", "Informe o usu�rio e a senha!", this);
		} else {
			dialog = ProgressDialog.show(Login.this, "Aguarde", "Conectando ao servidor..."); 
	        new Thread() {
	            public void run() {
	                try{
	                	conectarServidor();
	                } catch (Exception e) {
	                    Log.e("tag", e.getMessage());
	                }
	            }
	        }.start();
		}
	}
	
	public void onClickMostrarSenha(View view) {
		if (cbxMostrarSenha.isChecked()) {
			edtSenha.setInputType(InputType.TYPE_CLASS_TEXT);
		} else {
			edtSenha.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD);	
		}
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		switch (item.getItemId()) {
		case MENU_CONFIG:
			startActivity(new Intent(this, ConfiguracaoConexao.class));
			break;
		default:
			break;
		}
		return true;
	}

	@Override
	protected void onDestroy() {
		try {
			Conexao.getConexaoAtual().disconnect();
		} catch (Exception e) {
			e.printStackTrace();
		}
		super.onDestroy();
	}
	
	private void conectarServidor() {
		try {
			//String mac = "";
			//WifiManager wifiMgr = (WifiManager) this.getSystemService(Context.WIFI_SERVICE);
			//WifiInfo wifiInfo = wifiMgr.getConnectionInfo();
			//mac = wifiInfo.getBSSID();
			
			//Tratamento para funcionar em casa onde a Ponto Telecom n�o permite conex�o ao IP externo vindo da mesma rede
			//Assim n�o preciso trocar o tempo todo o IP/DNS
			//if ((mac != null) && (mac.equals("1c:af:f7:7e:c9:1e"))) {
			//	IP_SERVIDOR = "192.168.1.20";
			//} else {
			IP_SERVIDOR = Funcoes.carregarDadosComponente("edtHost", "", this);
			//}
			PORTA_SERVIDOR = Funcoes.carregarDadosComponente("edtPorta", "", this);
			
			Conexao conexao = Conexao.createConnection(IP_SERVIDOR, PORTA_SERVIDOR);
			conexao.conectar();

			try {
				Conexao.getConexaoAtual().iniciar();
			} catch (Exception e) {
				msgErro = "N�o foi poss�vel comunicar com o servidor.";
				Message msg = new Message();
				msg.arg1 = ERRO_CONEXAO;
				handler.sendMessage(msg);
				finish();
			}
			
			String mensagem = "";
			
			Document doc = new Document();
			Element root = new Element("Logar");
			         
			Element usuario = new Element("Usuario");
			usuario.setText(edtUsuario.getText().toString());
			root.addContent(usuario);
			
			Element senha = new Element("Senha");
			senha.setText(edtSenha.getText().toString());
			root.addContent(senha);
			doc.setRootElement(root);
			
			mensagem = new XMLOutputter().outputString(doc);				
			Conexao.getConexaoAtual().enviarMensagem(mensagem);
			mensagem = Conexao.getConexaoAtual().receberRetorno();  
			
			if (mensagem.equals("Logado")) {
				Funcoes.salvarDadosComponente("edtUsuario", edtUsuario.getText().toString(), this);
				
				if (cbxSalvarSenha.isChecked()) {
					Funcoes.salvarDadosComponente("edtSenha", edtSenha.getText().toString(), this);
					Funcoes.salvarDadosComponente("cbxSalvarSenha", "1", this);
				} else {
					Funcoes.salvarDadosComponente("edtSenha", "", this);
					Funcoes.salvarDadosComponente("cbxSalvarSenha", "0", this);
				}
				
				USUARIO = edtUsuario.getText().toString();
				SENHA = edtSenha.getText().toString();
				
				startActivity(new Intent(this, MenuPrincipal.class));
			} else if (mensagem.equals("NaoLogado")) {
				msgErro = "Usu�rio ou senha inv�lidos!";
				Message msg = new Message();
				msg.arg1 = ERRO_CONEXAO;
				handler.sendMessage(msg);
			}
			

		} catch (Exception e) {
			msgErro = "N�o foi poss�vel conectar: " + e.getMessage();
			Message msg = new Message();
			msg.arg1 = ERRO_CONEXAO;
			handler.sendMessage(msg);
		}
		dialog.dismiss();
	}
	
	@Override
	protected void onResume() {
		carregarComponentes();
		try {
			Conexao.getConexaoAtual().disconnect();
		} catch (Exception e) {
			e.printStackTrace();
		}
		super.onResume();
	}
}
