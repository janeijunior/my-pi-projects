package br.edu.unoesc;

import android.os.Bundle;
import android.app.Activity;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.ToggleButton;

public class ControleAlarme extends Activity implements OnClickListener {
	private ToggleButton btnAlarme;
	private ToggleButton btnPanico;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.controle_alarme);
		
		btnAlarme = (ToggleButton) findViewById(R.id.btnAlarme);
		btnAlarme.setOnClickListener(this);
		
		btnPanico = (ToggleButton) findViewById(R.id.btnPanico);
		btnPanico.setOnClickListener(this);
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.controle_alarme, menu);
		return true;
	}
	
	public void onClick(View view) {
		   if (view == btnAlarme) {
				if (btnAlarme.isChecked()) {
					ConnectionSocket.getCurentConnection().senMessage("la");
				} else {
					ConnectionSocket.getCurentConnection().senMessage("da");
				}
			} else if (view == btnPanico) {
				if (btnPanico.isChecked()) {
					ConnectionSocket.getCurentConnection().senMessage("lp");
				} else {
					ConnectionSocket.getCurentConnection().senMessage("dp");
				}
			}
		}

}
