package br.com.housepi.activity;

import br.com.housepi.R;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RelativeLayout;

public class ConfiguracaoAlarme extends Fragment {
	
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
		
		if (container == null) {
			return null;
		}

		return (RelativeLayout) inflater.inflate(R.layout.configuracao_alarme, container, false);
	}

}
