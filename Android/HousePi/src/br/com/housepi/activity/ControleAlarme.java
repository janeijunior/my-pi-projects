package br.com.housepi.activity;

import br.com.housepi.R;
import br.com.housepi.classes.Alarme;
import br.com.housepi.classes.Funcoes;
import android.os.Bundle;
import android.content.Context;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.ToggleButton;

public class ControleAlarme extends Fragment implements OnClickListener {
	private Alarme alarme;

	public static Fragment newInstance(Context context) {
		ControleAlarme f = new ControleAlarme();
		return f;
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.controle_alarme, container, false);

		alarme = new Alarme((ToggleButton) rootView.findViewById(R.id.btnAlarme), (ToggleButton) rootView.findViewById(R.id.btnPanico));
		alarme.getBtnAlarme().setOnClickListener(this);
		alarme.getBtnPanico().setOnClickListener(this);
		
		alarme.getConfiguracaoStatus();
		
		return rootView;
	}

	public void onClick(View view) {
		if (view == alarme.getBtnAlarme()) {
			if (alarme.getBtnAlarme().isChecked()) {
				if (!alarme.ligarAlarme()) {
					Funcoes.msgToastErroComando(this.getActivity());
					alarme.getBtnAlarme().setChecked(false);
				}
			} else {
				if (!alarme.desligarAlarme()) {
					Funcoes.msgToastErroComando(this.getActivity());
					alarme.getBtnAlarme().setChecked(true);
				}
			}	
			
		} else if (view == alarme.getBtnPanico()) {
			if (alarme.getBtnPanico().isChecked()) {
				if (!alarme.ligarPanico()) {
					Funcoes.msgToastErroComando(this.getActivity());
					alarme.getBtnPanico().setChecked(false);
				}
			} else {
				if (!alarme.desligarPanico()) {
					Funcoes.msgToastErroComando(this.getActivity());
					alarme.getBtnPanico().setChecked(true);
				}
			}
		}
	}
	
	
}
