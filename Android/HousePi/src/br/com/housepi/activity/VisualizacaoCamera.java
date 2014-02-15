package br.com.housepi.activity;

import java.io.IOException;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;

import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.output.XMLOutputter;

import br.com.housepi.activity.Login;
import android.content.Context;
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
	private HttpURLConnection con;

	public static Fragment newInstance(Context context) {
		VisualizacaoCamera f = new VisualizacaoCamera();
		return f;
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.visualizacao_camera, container, false);

		controlarCamera("Ligar");
		
		mv = (MjpegView) rootView.findViewById(R.id.mjpeg_view);
		
		String url = "http://" + Login.IP_SERVIDOR + ":5005/?action=stream"; 

		mv = (MjpegView) rootView.findViewById(R.id.mjpeg_view);
		connection(mv, url);

		return rootView;
	}

	private void connection(MjpegView mv, String url) {
		try {
			URL addr = new URL(url);
			con = (HttpURLConnection) addr.openConnection();
			con.connect();
			InputStream stream;
			stream = con.getInputStream();
			mv.setSource(new MjpegInputStream(stream));
			mv.setDisplayMode(MjpegView.SIZE_BEST_FIT);
			mv.showFps(false);
		} catch (IOException e) {
			e.printStackTrace();
		}
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
	
	@Override
	public void onPause() {
		con.disconnect();
		controlarCamera("Desligar");
		super.onPause();
	}
}
