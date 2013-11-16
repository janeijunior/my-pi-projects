package br.edu.unoesc;

import android.os.Bundle;
import android.preference.PreferenceManager;
import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.SharedPreferences.Editor;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;

public class ConfigurarConexao extends Activity implements OnClickListener {
	private EditText edtHost;
	private EditText edtPorta;
	private Button btnSalvar;


	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.configurar_conexao);
		
		btnSalvar = (Button) findViewById(R.id.btnSalvarConfiguracao);
		btnSalvar.setOnClickListener(this);
	
		edtHost = (EditText) findViewById(R.id.edtHost);
		edtPorta = (EditText) findViewById(R.id.edtPorta);

		edtHost.setText(carregarPreferencias("edtHost", edtHost.getText().toString()));
		edtPorta.setText(carregarPreferencias("edtPorta", edtPorta.getText().toString()));
	}
	
	private void salvarPreferencias(String key, String value) {
		        SharedPreferences sharedPreferences = PreferenceManager.getDefaultSharedPreferences(this);
		        Editor editor = sharedPreferences.edit();
		        editor.putString(key, value);
		        editor.commit();
		    }
	
	private String carregarPreferencias(String key, String value) {
		SharedPreferences sharedPreferences = PreferenceManager.getDefaultSharedPreferences(this);
		return sharedPreferences.getString(key, value);       
	}


	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.configurar_conexao, menu);
		return true;
	}

	public void onClick(View view) {
		   if (view == btnSalvar) {
				salvarPreferencias("edtHost", edtHost.getText().toString());
				salvarPreferencias("edtPorta", edtPorta.getText().toString());
				
				startActivity(new Intent(this, Login.class));
		   } 
		}
}
