package br.com.housepi.activity;

import java.io.IOException;
import java.net.URI;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.DefaultHttpClient;
import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.output.XMLOutputter;
import br.com.housepi.activity.Login;
import android.content.Context;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import br.com.housepi.R;
import br.com.housepi.bibliotecas.MjpegInputStream;
import br.com.housepi.bibliotecas.MjpegView;
import br.com.housepi.classes.Conexao;

public class VisualizacaoCamera extends Fragment {

	private MjpegView mv;

	public static Fragment newInstance(Context context) {
		VisualizacaoCamera f = new VisualizacaoCamera();
		return f;
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.visualizacao_camera, container, false);

		Integer portaCamera = Integer.parseInt(Login.PORTA_SERVIDOR) + 1;
		String URL = "http://" + Login.IP_SERVIDOR + ":" + portaCamera.toString() + "/?action=stream";
		
		mv = (MjpegView) rootView.findViewById(R.id.mjpeg_view);
		
		new DoRead().execute(URL);

		return rootView;
	}

	public void onPause() {
		mv.stopPlayback();
		controlarCamera("Desligar");
		super.onPause();		
	}
	
	private void controlarCamera(String comando){
		Document doc = new Document();
		Element root = new Element("ControlarCamera");
		       
		Element acao = new Element("Acao");	
		
		acao.setText(comando);
		
		root.addContent(acao);
		doc.setRootElement(root);
		Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));
		
		Conexao.getConexaoAtual().receberRetorno().equals("Ok");
	}

	public class DoRead extends AsyncTask<String, Void, MjpegInputStream> {
		protected MjpegInputStream doInBackground(String... url) {
			HttpResponse res = null;
			DefaultHttpClient httpclient = new DefaultHttpClient();
			try {
				controlarCamera("Ligar");
				
				res = httpclient.execute(new HttpGet(URI.create(url[0])));
				if (res.getStatusLine().getStatusCode() == 401) {
					return null;
				}
				return new MjpegInputStream(res.getEntity().getContent());
			} catch (ClientProtocolException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}

			return null;
		}

		protected void onPostExecute(MjpegInputStream result) {
			mv.setSource(result);
			mv.setDisplayMode(MjpegView.SIZE_BEST_FIT);
			mv.showFps(false);
		}
	}
}
