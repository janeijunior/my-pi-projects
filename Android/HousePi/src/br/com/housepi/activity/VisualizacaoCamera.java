package br.com.housepi.activity;

import java.io.IOException;
import java.net.URI;
import java.util.ArrayList;
import java.util.List;
import org.apache.http.HttpResponse;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.CredentialsProvider;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.apache.http.impl.client.DefaultHttpClient;
import br.com.housepi.activity.Login;
import android.content.Context;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemSelectedListener;
import android.widget.ArrayAdapter;
import android.widget.LinearLayout;
import android.widget.Spinner;
import br.com.housepi.R;
import br.com.housepi.bibliotecas.MjpegInputStream;
import br.com.housepi.bibliotecas.MjpegView;

public class VisualizacaoCamera extends Fragment implements OnItemSelectedListener {

	private MjpegView mv;
	private Spinner spinner;
	private LinearLayout llCamera;
	
	public static Fragment newInstance(Context context) {
		VisualizacaoCamera f = new VisualizacaoCamera();
		return f;
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.visualizacao_camera, container, false);
	
		llCamera = (LinearLayout) rootView.findViewById(R.id.llCamera);
		
		spinner = (Spinner) rootView.findViewById(R.id.spCamera); 
        spinner.setOnItemSelectedListener(this);
 
        List<String> cameras = new ArrayList<String>();
        cameras.add("Câmera 1");
        cameras.add("Câmera 2");
 
        ArrayAdapter<String> dataAdapter = new ArrayAdapter<String>(rootView.getContext(), android.R.layout.simple_spinner_item, cameras);
        dataAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        spinner.setAdapter(dataAdapter);
        
		return rootView;
	}

	private void conectar(String url) {
		try {
			HttpResponse res = null;
			DefaultHttpClient httpclient = new DefaultHttpClient();
			
			CredentialsProvider credProvider = new BasicCredentialsProvider();
		    credProvider.setCredentials(new AuthScope(AuthScope.ANY_HOST, AuthScope.ANY_PORT), new UsernamePasswordCredentials(Login.USUARIO, Login.SENHA));
		    
		    httpclient.setCredentialsProvider(credProvider);
			
			res = httpclient.execute(new HttpGet(URI.create(url)));

			mv.setSource(new MjpegInputStream(res.getEntity().getContent()));
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
		
	@Override
	public void onPause() {
		mv.destroyDrawingCache();
		mv.stopPlayback();
		super.onPause();
	}

	@Override
	public void onItemSelected(AdapterView<?> arg0, View arg1, int arg2, long arg3) {
		if (mv != null) {
			mv.destroyDrawingCache();
			mv.stopPlayback();
			llCamera.removeView(mv);
		}
		
		mv = new MjpegView(this.getActivity());
		llCamera.addView(mv);
		mv.setDisplayMode(MjpegView.SIZE_BEST_FIT);
		mv.showFps(false);

		Integer portaCamera;
		
		if (spinner.getSelectedItemPosition() == 0) {
			portaCamera = Integer.parseInt(Login.PORTA_SERVIDOR) + 1;
		} else {
			portaCamera = Integer.parseInt(Login.PORTA_SERVIDOR) + 2;
		}
		
		String url = "http://" + Login.IP_SERVIDOR + ":" + portaCamera.toString() + "/?action=stream";
		conectar(url);
	}

	@Override
	public void onNothingSelected(AdapterView<?> arg0) {
		
	}
}
