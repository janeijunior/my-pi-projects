package br.com.housepi.activity;

import br.com.housepi.R;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

public class Sobre extends Fragment {

	public static Fragment newInstance(Context context) {
		Sobre f = new Sobre();
		return f;
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.sobre, container, false);
		
		return rootView;
	}
}
