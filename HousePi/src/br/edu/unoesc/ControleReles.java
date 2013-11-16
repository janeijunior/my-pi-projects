package br.edu.unoesc;

import android.os.Bundle;
import android.app.Activity;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.ToggleButton;

public class ControleReles extends Activity implements OnClickListener {
	private ToggleButton btnRele1;
	private ToggleButton btnRele2;
	private ToggleButton btnRele3;
	private ToggleButton btnRele4;
	private ToggleButton btnRele5;
	private ToggleButton btnRele6;
	private ToggleButton btnRele7;
	private ToggleButton btnRele8;
	private ToggleButton btnRele9;
	private ToggleButton btnRele10;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.controle_reles);
		
		btnRele1 = (ToggleButton) findViewById(R.id.btnRele1);
		btnRele1.setOnClickListener(this);

		btnRele2 = (ToggleButton) findViewById(R.id.btnRele2);
		btnRele2.setOnClickListener(this);

		btnRele3 = (ToggleButton) findViewById(R.id.btnRele3);
		btnRele3.setOnClickListener(this);

		btnRele4 = (ToggleButton) findViewById(R.id.btnRele4);
		btnRele4.setOnClickListener(this);

		btnRele5 = (ToggleButton) findViewById(R.id.btnRele5);
		btnRele5.setOnClickListener(this);

		btnRele6 = (ToggleButton) findViewById(R.id.btnRele6);
		btnRele6.setOnClickListener(this);

		btnRele7 = (ToggleButton) findViewById(R.id.btnRele7);
		btnRele7.setOnClickListener(this);

		btnRele8 = (ToggleButton) findViewById(R.id.btnRele8);
		btnRele8.setOnClickListener(this);

		btnRele9 = (ToggleButton) findViewById(R.id.btnRele9);
		btnRele9.setOnClickListener(this);

		btnRele10 = (ToggleButton) findViewById(R.id.btnRele10);
		btnRele10.setOnClickListener(this);
	}
	
	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.controle_reles, menu);
		return true;
	}
	
	public void onClick(View view) {
		if (view == btnRele1) { 		
			if (btnRele1.isChecked()) {
				ConnectionSocket.getCurentConnection().senMessage("l0");
			} else {
				ConnectionSocket.getCurentConnection().senMessage("d0");
			}			
		} else if (view == btnRele2) {
			if (btnRele2.isChecked()) {
				ConnectionSocket.getCurentConnection().senMessage("l1");
			} else {
				ConnectionSocket.getCurentConnection().senMessage("d1");
			}
		} else if (view == btnRele3) {
			if (btnRele3.isChecked()) {
				ConnectionSocket.getCurentConnection().senMessage("l2");
			} else {
				ConnectionSocket.getCurentConnection().senMessage("d2");
			}
		} else if (view == btnRele4) {
			if (btnRele4.isChecked()) {
				ConnectionSocket.getCurentConnection().senMessage("l3");
			} else {
				ConnectionSocket.getCurentConnection().senMessage("d3");
			}
		} else if (view == btnRele5) {
			if (btnRele5.isChecked()) {
				ConnectionSocket.getCurentConnection().senMessage("l4");
			} else {
				ConnectionSocket.getCurentConnection().senMessage("d4");
			}
		} else if (view == btnRele6) {
			if (btnRele6.isChecked()) {
				ConnectionSocket.getCurentConnection().senMessage("l5");
			} else {
				ConnectionSocket.getCurentConnection().senMessage("d5");
			}
		} else if (view == btnRele7) {
			if (btnRele7.isChecked()) {
				ConnectionSocket.getCurentConnection().senMessage("l6");
			} else {
				ConnectionSocket.getCurentConnection().senMessage("d6");
			}
		} else if (view == btnRele8) {
			if (btnRele8.isChecked()) {
				ConnectionSocket.getCurentConnection().senMessage("l7");
			} else {
				ConnectionSocket.getCurentConnection().senMessage("d7");
			}
		} else if (view == btnRele9) {
			if (btnRele9.isChecked()) {
				ConnectionSocket.getCurentConnection().senMessage("l8");
			} else {
				ConnectionSocket.getCurentConnection().senMessage("d8");
			}
		} else if (view == btnRele10) {
			if (btnRele10.isChecked()) {
				ConnectionSocket.getCurentConnection().senMessage("l9");
			} else {
				ConnectionSocket.getCurentConnection().senMessage("d9");
			}
		} 
	}

}
