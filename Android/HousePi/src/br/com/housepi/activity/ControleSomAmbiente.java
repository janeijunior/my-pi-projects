package br.com.housepi.activity;

import br.com.housepi.R;
import android.os.Bundle;
import android.content.Context;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

public class ControleSomAmbiente extends Fragment  {

    public static Fragment newInstance(Context context) {
    	ControleSomAmbiente f = new ControleSomAmbiente();
        return f;
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.controle_som_ambiente, container, false);

        return rootView;
    }

}
