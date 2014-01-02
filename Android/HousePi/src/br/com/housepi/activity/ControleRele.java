package br.com.housepi.activity;

import java.util.ArrayList;
import java.util.List;

import br.com.housepi.R;
import br.com.housepi.classes.Funcoes;
import br.com.housepi.classes.Rele;
import android.os.Bundle;
import android.content.Context;
import android.annotation.SuppressLint;
import android.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.ToggleButton;

@SuppressLint("NewApi")
public class ControleRele extends Fragment implements OnClickListener {
	private List<Rele> listaReles = new ArrayList<Rele>();

	public static Fragment newInstance(Context context) {
		ControleRele f = new ControleRele();
		return f;
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.controle_reles, container, false);

		Rele rele;

		rele = new Rele(0, (ToggleButton) rootView.findViewById(R.id.btnRele0));
		rele.getBotao().setOnClickListener(this);
		listaReles.add(rele);

		rele = new Rele(1, (ToggleButton) rootView.findViewById(R.id.btnRele1));
		rele.getBotao().setOnClickListener(this);
		listaReles.add(rele);

		rele = new Rele(2, (ToggleButton) rootView.findViewById(R.id.btnRele2));
		rele.getBotao().setOnClickListener(this);
		listaReles.add(rele);

		rele = new Rele(3, (ToggleButton) rootView.findViewById(R.id.btnRele3));
		rele.getBotao().setOnClickListener(this);
		listaReles.add(rele);

		rele = new Rele(4, (ToggleButton) rootView.findViewById(R.id.btnRele4));
		rele.getBotao().setOnClickListener(this);
		listaReles.add(rele);

		rele = new Rele(5, (ToggleButton) rootView.findViewById(R.id.btnRele5));
		rele.getBotao().setOnClickListener(this);
		listaReles.add(rele);

		rele = new Rele(6, (ToggleButton) rootView.findViewById(R.id.btnRele6));
		rele.getBotao().setOnClickListener(this);
		listaReles.add(rele);

		rele = new Rele(7, (ToggleButton) rootView.findViewById(R.id.btnRele7));
		rele.getBotao().setOnClickListener(this);
		listaReles.add(rele);

		rele = new Rele(8, (ToggleButton) rootView.findViewById(R.id.btnRele8));
		rele.getBotao().setOnClickListener(this);
		listaReles.add(rele);

		rele = new Rele(9, (ToggleButton) rootView.findViewById(R.id.btnRele9));
		rele.getBotao().setOnClickListener(this);
		listaReles.add(rele);

		listaReles = Rele.getConfiguracaoStatus(listaReles);

		return rootView;
	}

	public void onClick(View view) {

		for (Rele rele : listaReles) {
			if (view == rele.getBotao()) {
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
}
