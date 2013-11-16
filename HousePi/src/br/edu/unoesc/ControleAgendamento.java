package br.edu.unoesc;

import android.os.Bundle;
import android.app.Activity;
import android.view.Menu;

public class ControleAgendamento extends Activity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.controle_agendamento);
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.controle_agendamento, menu);
		return true;
	}

}
