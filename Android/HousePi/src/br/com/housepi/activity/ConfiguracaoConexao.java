package br.com.housepi.activity;

import br.com.housepi.R;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.View;
import android.widget.EditText;
import br.com.housepi.classes.Funcoes;

public class ConfiguracaoConexao extends ActionBarActivity {
	private EditText edtHost;
	private EditText edtPorta;


	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.configuracao_conexao);
	
		edtHost = (EditText) findViewById(R.id.edtHost);
		edtPorta = (EditText) findViewById(R.id.edtPorta);

		edtHost.setText(Funcoes.carregarDadosComponente("edtHost", edtHost.getText().toString(), this));
		edtPorta.setText(Funcoes.carregarDadosComponente("edtPorta", edtPorta.getText().toString(), this));
	}
	

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		getMenuInflater().inflate(R.menu.configuracao_conexao, menu);
		return true;
	}
	
	public void onClickSalvar(View view) {
		Funcoes.salvarDadosComponente("edtHost", edtHost.getText().toString(), this);
		Funcoes.salvarDadosComponente("edtPorta", edtPorta.getText().toString(), this);
		
		this.finish();
	}
}
