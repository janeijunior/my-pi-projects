package br.com.housepi.activity;

import br.com.housepi.R;
import br.com.housepi.classes.Alarme;
import br.com.housepi.classes.Funcoes;
import android.os.AsyncTask;
import android.os.Bundle;
import android.content.Context;
import android.content.Intent;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.TextView;
import android.widget.ToggleButton;

public class ControleAlarme extends Fragment implements OnClickListener {
	private static Alarme alarme;
	private static Button btnDisparos;
	
	public static Fragment newInstance(Context context) {
		ControleAlarme f = new ControleAlarme();
		return f;
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.controle_alarme, container, false);

		btnDisparos = (Button) rootView.findViewById(R.id.btnDisparos);
		btnDisparos.setOnClickListener(this);
		
		alarme = new Alarme((ToggleButton) rootView.findViewById(R.id.btnAlarme), (ToggleButton) rootView.findViewById(R.id.btnPanico), (TextView) rootView.findViewById(R.id.lblStatus));
		alarme.getBtnAlarme().setOnClickListener(this);
		alarme.getBtnPanico().setOnClickListener(this);
		
		alarme.getConfiguracaoStatus();
		
		new AtualizaTela().execute();
		
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
		} else if (view == btnDisparos) {
			startActivity(new Intent(this.getActivity(), VisualizacaoDisparos.class));
		}
	}
	
	public static void comandoVoz(String comando, Context contexto){
		if (comando.trim().equalsIgnoreCase("Alarme")) {
			alarme.getBtnAlarme().performClick();
		} else if (comando.trim().equalsIgnoreCase("Pânico")) {
			alarme.getBtnPanico().performClick();
		} else if ((comando.trim().equalsIgnoreCase("Últimos Disparos")) || (comando.trim().equalsIgnoreCase("Disparos"))) {
			btnDisparos.performClick();
		}
	}
	
	private class AtualizaTela extends AsyncTask<Void, Void, Void> {
		@Override
        protected Void doInBackground(Void... voids) {
			try{    
                Thread.sleep(10000);
            }catch(InterruptedException e){
                e.printStackTrace();
            }
			
            return null;
        }

        protected void onPostExecute(Void result) {
        	alarme.getConfiguracaoStatus();
    		
        	new AtualizaTela().execute();
        }
    }
}
