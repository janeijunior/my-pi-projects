package br.com.housepi.activity;

import java.util.ArrayList;
import java.util.List;
import br.com.housepi.R;
import br.com.housepi.classes.Funcoes;
import br.com.housepi.classes.Rele;
import android.os.AsyncTask;
import android.os.Bundle;
import android.annotation.SuppressLint;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.View.OnLongClickListener;
import android.view.ViewGroup;
import android.widget.NumberPicker;
import android.widget.RelativeLayout;
import android.widget.Toast;
import android.widget.ToggleButton;

public class ControleRele extends Fragment implements OnClickListener, OnLongClickListener {
	private static List<Rele> listaReles = new ArrayList<Rele>();
	private Rele releTemporizador; 
	
	public static Fragment newInstance(Context context) {
		ControleRele f = new ControleRele();
		return f;
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.controle_reles, container, false);

		Rele rele;
		
		listaReles.clear();
		
		rele = new Rele(0, (ToggleButton) rootView.findViewById(R.id.btnRele0));
		rele.getBotao().setOnClickListener(this);
		rele.getBotao().setOnLongClickListener(this);
		listaReles.add(rele);

		rele = new Rele(1, (ToggleButton) rootView.findViewById(R.id.btnRele1));
		rele.getBotao().setOnClickListener(this);
		rele.getBotao().setOnLongClickListener(this);
		listaReles.add(rele);

		rele = new Rele(2, (ToggleButton) rootView.findViewById(R.id.btnRele2));
		rele.getBotao().setOnClickListener(this);
		rele.getBotao().setOnLongClickListener(this);
		listaReles.add(rele);

		rele = new Rele(3, (ToggleButton) rootView.findViewById(R.id.btnRele3));
		rele.getBotao().setOnClickListener(this);
		rele.getBotao().setOnLongClickListener(this);
		listaReles.add(rele);

		rele = new Rele(4, (ToggleButton) rootView.findViewById(R.id.btnRele4));
		rele.getBotao().setOnClickListener(this);
		rele.getBotao().setOnLongClickListener(this);
		listaReles.add(rele);

		rele = new Rele(5, (ToggleButton) rootView.findViewById(R.id.btnRele5));
		rele.getBotao().setOnClickListener(this);
		rele.getBotao().setOnLongClickListener(this);
		listaReles.add(rele);

		rele = new Rele(6, (ToggleButton) rootView.findViewById(R.id.btnRele6));
		rele.getBotao().setOnClickListener(this);
		rele.getBotao().setOnLongClickListener(this);
		listaReles.add(rele);

		rele = new Rele(7, (ToggleButton) rootView.findViewById(R.id.btnRele7));
		rele.getBotao().setOnClickListener(this);
		rele.getBotao().setOnLongClickListener(this);
		listaReles.add(rele);

		rele = new Rele(8, (ToggleButton) rootView.findViewById(R.id.btnRele8));
		rele.getBotao().setOnClickListener(this);
		rele.getBotao().setOnLongClickListener(this);
		listaReles.add(rele);

		rele = new Rele(9, (ToggleButton) rootView.findViewById(R.id.btnRele9));
		rele.getBotao().setOnClickListener(this);
		rele.getBotao().setOnLongClickListener(this);
		listaReles.add(rele);

		listaReles = Rele.getConfiguracaoStatus(listaReles);

		new AtualizaTela().execute();
		
		return rootView;
	}

	public void onClick(View view) {

		for (Rele rele : listaReles) {
			if (view == rele.getBotao()) {
				rele.setTemporizador(0);
				
				if (rele.getBotao().isChecked()) {
					if (!rele.ligar()) {
						Funcoes.msgToastErroComando(this.getActivity());
						rele.getBotao().setChecked(false);
					}
				} else {
					if (!rele.desligar()) {
						Funcoes.msgToastErroComando(this.getActivity());
						rele.getBotao().setChecked(true);
					}
				}
			}
		}
	}

	public boolean onLongClick(View view) {
		if (android.os.Build.VERSION.SDK_INT >= 11) {
			for (Rele rele : listaReles) {
				if (view == rele.getBotao()) {
					if (!rele.getBotao().isChecked()) {
						releTemporizador = rele;
						mostrarTemporizador();
					} 
				}
			}
		}
		
		return true;
	}
	
	public static void comandoVoz(String comando, Context contexto){
		for (Rele rele : listaReles) {
			if (comando.trim().equalsIgnoreCase(rele.getNome())) {
				rele.getBotao().performClick();
			}
		}
	}
	
	@SuppressLint("NewApi")
	public void mostrarTemporizador()
    {
		RelativeLayout linearLayout = new RelativeLayout(getActivity());
        final NumberPicker aNumberPicker = new NumberPicker(getActivity());
        aNumberPicker.setMaxValue(1440);
        aNumberPicker.setMinValue(1);
        aNumberPicker.setValue(1);

        RelativeLayout.LayoutParams params = new RelativeLayout.LayoutParams(50, 50);
        RelativeLayout.LayoutParams numPicerParams = new RelativeLayout.LayoutParams(RelativeLayout.LayoutParams.WRAP_CONTENT, RelativeLayout.LayoutParams.WRAP_CONTENT);
        numPicerParams.addRule(RelativeLayout.CENTER_HORIZONTAL);

        linearLayout.setLayoutParams(params);
        linearLayout.addView(aNumberPicker, numPicerParams);

        AlertDialog.Builder alertDialogBuilder = new AlertDialog.Builder(getActivity());
        alertDialogBuilder.setTitle("Informe o tempo (em minutos) para que o relé permaneça ligado");
        alertDialogBuilder.setView(linearLayout);
        alertDialogBuilder.setCancelable(false)
        	.setPositiveButton("Confirmar", new DialogInterface.OnClickListener() {
                	public void onClick(DialogInterface dialog, int id) {
                        
                		aNumberPicker.clearFocus();
                		
                		releTemporizador.getBotao().setChecked(true);
        				releTemporizador.setTemporizador(aNumberPicker.getValue());
        				
        				if (!releTemporizador.ligar()) {
        					Funcoes.msgToastErroComando(getActivity());
        					releTemporizador.getBotao().setChecked(false);
        				} else {
        					Toast.makeText(getActivity(), releTemporizador.getNome() + " temporizado para " + 
        				      releTemporizador.getTemporizador().toString() + " minuto(s).", Toast.LENGTH_SHORT).show();
        				}
                	}
    			})
    		.setNegativeButton("Cancelar", new DialogInterface.OnClickListener() {
    				public void onClick(DialogInterface dialog, int id) {
    					dialog.cancel();
    				}
            });
        
        AlertDialog alertDialog = alertDialogBuilder.create();
        alertDialog.show();
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
        	listaReles = Rele.getConfiguracaoStatus(listaReles);
        	
        	new AtualizaTela().execute();
        }
    }
}
