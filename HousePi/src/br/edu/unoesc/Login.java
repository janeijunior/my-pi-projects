package br.edu.unoesc;

import android.os.Bundle;
import android.os.Handler;
import android.preference.PreferenceManager;
import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;
import android.view.View.OnClickListener;

public class Login extends Activity implements OnClickListener {
	private Button btnConectar;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.login);
		
		btnConectar = (Button) findViewById(R.id.btnConectar);
		btnConectar.setOnClickListener(this);
	}
	
	@SuppressLint("HandlerLeak")
	private Handler handler = new Handler() {
		public void handleMessage(android.os.Message msg) {
			synchronized (msg) {
				switch (msg.arg1) {
				case ConnectionSocket.CONNECTED:
					
					break;
				case ConnectionSocket.SENDING_MESSAGE:
					
					break;
				case ConnectionSocket.ERROR:
					
					break;
				case ConnectionSocket.DISCONNECTED:
					
					break;
				
				case ConnectionSocket.RECEIVED_MESSAGE:
					
					break;
				}
			}
		};

	};

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		menu.add(0, 1, 0, "Configuração");
		return true;
	}
	
	@Override
	public void onClick(View view) {
		if (view == btnConectar) {
			try {
				ConnectionSocket conexao = ConnectionSocket.createConnection(carregarPreferencias("edtHost", ""), carregarPreferencias("edtPorta", ""));
				conexao.connect();
				
				try {
					ConnectionSocket.getCurentConnection().startSender(handler);
				} catch (Exception e) {
					Toast.makeText(this, "Não foi possível comunicar com o servidor.", Toast.LENGTH_LONG).show();
					finish();
				}	
				
				
				startActivity(new Intent(this, MenuPrincipal.class));
				
			} catch (Exception e) {
				Toast.makeText(this, "Não foi possível conectar: " + e.getMessage(), Toast.LENGTH_LONG).show();
			}
		}
	}
	
	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		switch(item.getItemId()) {
		case 1:
			startActivity(new Intent(this, ConfigurarConexao.class));
			break;
		default:
			break;
		}
		return true;
	}
	
	private String carregarPreferencias(String key, String value) {
		SharedPreferences sharedPreferences = PreferenceManager.getDefaultSharedPreferences(this);
		return sharedPreferences.getString(key, value);       
	}
	
	@Override
	protected void onDestroy() {
		try {
			ConnectionSocket.getCurentConnection().disconnect();
		} catch (Exception e) {
			e.printStackTrace();
		}
		super.onDestroy();
	}
	
}
