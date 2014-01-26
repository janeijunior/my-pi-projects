package br.com.housepi.activity;

import br.com.housepi.R;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.content.Context;
import android.content.pm.PackageManager.NameNotFoundException;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

public class Sobre extends Fragment {
	private TextView lblVersao;
	
	public static Fragment newInstance(Context context) {
		Sobre f = new Sobre();
		return f;
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.sobre, container, false);
		
		lblVersao = (TextView) rootView.findViewById(R.id.lblVersao);
		
		try {
			lblVersao.setText(this.getActivity().getPackageManager().getPackageInfo(this.getActivity().getPackageName(), 0).versionName);
		} catch (NameNotFoundException e) {
			lblVersao.setText("Indisponível");
		}
		
		return rootView;
	}
}
