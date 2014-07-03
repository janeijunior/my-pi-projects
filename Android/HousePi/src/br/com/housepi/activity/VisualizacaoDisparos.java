package br.com.housepi.activity;

import java.io.IOException;
import java.io.Reader;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.JDOMException;
import org.jdom2.input.SAXBuilder;
import org.jdom2.output.XMLOutputter;
import br.com.housepi.R;
import br.com.housepi.classes.Conexao;
import br.com.housepi.classes.Funcoes;
import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.widget.ListView;
import android.widget.SimpleAdapter;

public class VisualizacaoDisparos extends ActionBarActivity {
	private ListView listView;
	private SimpleAdapter adapter;
	private static final ArrayList<HashMap<String,String>> disparos = new ArrayList<HashMap<String,String>>(); 
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.visualizacao_disparos);
		
		listView = (ListView) findViewById(R.id.listDisparo);
		
		adapter = new SimpleAdapter(
        		this,
        		disparos,
        		R.layout.linha_list_view_disparo,
        		new String[] {"Sensor", "DataHora"},
        		new int[] {R.id.listNomeSensor, R.id.listDataHora}
        		);
		
		listView.setAdapter(adapter);
		
		getUltimosDisparos();
	}
	
	private void getUltimosDisparos() {
		Document doc = new Document();
		String mensagem = "";
		
		Element root = new Element("EnviarUltimosDisparos");
		doc.setRootElement(root);

		Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));

		mensagem = Conexao.getConexaoAtual().receberRetorno();
					
		SAXBuilder builder = new SAXBuilder();
		Reader in = new StringReader(mensagem);

		try {
			doc = builder.build(in);
		} catch (JDOMException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		Element retorno = (Element) doc.getRootElement();
		
		disparos.clear();
		
		if (retorno.getName().equals("EnviarUltimosDisparos")) {
			@SuppressWarnings("rawtypes")
			List elements = retorno.getChildren();
			@SuppressWarnings("rawtypes")
			Iterator j = elements.iterator();
	
			while (j.hasNext()) {
				Element element = (Element) j.next();
				addListaDisparo(element.getAttribute("NomeSensor").getValue(), Funcoes.formatarDataHoraLocal((Funcoes.formatarDataHora(element.getAttribute("DataHora").getValue()))));
			}
		}
			
		adapter.notifyDataSetChanged();
	}
	
	private void addListaDisparo(String nome, String dataHora) {
    	HashMap<String,String> temp = new HashMap<String,String>();
    	if (nome.length() > 20) {
    		temp.put("Sensor", nome.substring(0, 20) + "...");
    	} else {
    		temp.put("Sensor", nome);
    	}
    	temp.put("DataHora", dataHora);
    	disparos.add(temp);
    }

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		getMenuInflater().inflate(R.menu.visualizacao_disparos, menu);
		return true;
	}

}
