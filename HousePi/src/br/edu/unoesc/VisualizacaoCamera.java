package br.edu.unoesc;

import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

import android.app.Activity;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.view.Menu;
import br.edu.unoesc.MjpegInputStream;
import br.edu.unoesc.MjpegView;

public class VisualizacaoCamera extends Activity {
	
	private MjpegView mv;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.visualizacao_camera);
        mv = (MjpegView) findViewById(R.id.mjpeg_view);
		
		ConnectionSocket.getCurentConnection().senMessage("lc");
		
		try {
			Thread.sleep(2000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		
        String url = "http://" + carregarPreferencias("edtHost", "") + ":5005/?action=stream"; 
        
        mv = (MjpegView) findViewById(R.id.mjpeg_view);
        connection(mv, url);
	}

	 private void connection(MjpegView mv, String url) {
         try {
                 URL addr = new URL(url);
                 HttpURLConnection con = (HttpURLConnection) addr.openConnection();
                 con.connect();
                 InputStream stream;
                 stream = con.getInputStream();
                 mv.setSource(new MjpegInputStream(stream));
                 mv.setDisplayMode(MjpegView.SIZE_BEST_FIT);
                 mv.showFps(true);
         } catch (IOException e) {
                 e.printStackTrace();
         }
 }
	 
	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.visualizacao_camera, menu);
		return true;
	}
	
	private String carregarPreferencias(String key, String value) {
		SharedPreferences sharedPreferences = PreferenceManager.getDefaultSharedPreferences(this);
		return sharedPreferences.getString(key, value);       
	}
	
	@Override
	protected void onDestroy() {
		ConnectionSocket.getCurentConnection().senMessage("dc");
		
		try {
			Thread.sleep(2000);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		
		super.onDestroy();
	}

}
