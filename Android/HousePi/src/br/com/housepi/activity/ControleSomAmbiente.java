package br.com.housepi.activity;

import java.io.Reader;
import java.io.StringReader;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.JDOMException;
import org.jdom2.input.SAXBuilder;
import org.jdom2.output.XMLOutputter;
import br.com.housepi.R;
import br.com.housepi.classes.Conexao;
import android.os.Bundle;
import android.content.Context;
import android.support.v4.app.Fragment;
import android.view.ContextMenu;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.view.ContextMenu.ContextMenuInfo;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.Toast;

public class ControleSomAmbiente extends Fragment {
	private ListView listView;
	private ArrayAdapter<String> adapter;
	private List<String> musicas = new LinkedList<String>();
	private String[] menuItems = new String[] {"Executar"};

	public static Fragment newInstance(Context context) {
		ControleSomAmbiente f = new ControleSomAmbiente();
		return f;
	}

	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
		View rootView = inflater.inflate(R.layout.controle_som_ambiente,
				container, false);

		listView = (ListView) rootView.findViewById(R.id.listMusica);

		adapter = new ArrayAdapter<String>(this.getActivity(), android.R.layout.simple_list_item_1, android.R.id.text1, musicas);

		listView.setAdapter(adapter);
		registerForContextMenu(listView);
		
		getMusicas();

		return rootView;
	}
	
	@Override
	public void onCreateContextMenu(ContextMenu menu, View v,
	    ContextMenuInfo menuInfo) {
	  if (v.getId( )== R.id.listMusica) {
	    menu.setHeaderTitle("O que deseja fazer?");
	    
	    for (int i = 0; i < menuItems.length; i++) {
	      menu.add(Menu.NONE, i, i, menuItems[i]);
	    }
	  }
	}
	
	@Override
	public boolean onContextItemSelected(MenuItem item) {
		AdapterView.AdapterContextMenuInfo info = (AdapterView.AdapterContextMenuInfo)item.getMenuInfo();
		//int menuItemIndex = item.getItemId();
		//String menuItemName = menuItems[menuItemIndex];
	  
		String musica = musicas.get(info.position).toString();
	 
		Document doc = new Document();
		Element root = new Element("ExecutarMusica").setText(musica);
		doc.setRootElement(root);
	
		Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));
	  
	  return true;
	}

	@SuppressWarnings("deprecation")
	private void getMusicas() {
		try {
			Document doc = new Document();
			Element root = new Element("EnviarListaMusica");
			doc.setRootElement(root);
	
			Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));
	
			String mensagem = "";
			musicas.clear();
	
			mensagem = Conexao.getConexaoAtual().getIn().readLine();
	
			SAXBuilder builder = new SAXBuilder();
			Reader in = new StringReader(mensagem);
	
			try {
				doc = builder.build(in);
			} catch (JDOMException e) {
				e.printStackTrace();
			}
	
			Element retorno = (Element) doc.getRootElement();
			
			@SuppressWarnings("rawtypes")
			List elements = retorno.getChildren();
			@SuppressWarnings("rawtypes")
			Iterator j = elements.iterator();
			
			while (j.hasNext()) {
				Element element = (Element) j.next();
				musicas.add(element.getAttribute("Nome").getValue());
			}
			
			adapter.notifyDataSetChanged();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
