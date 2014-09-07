package br.com.housepi.activity;

import java.io.IOException;
import java.io.Reader;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.JDOMException;
import org.jdom2.input.SAXBuilder;
import org.jdom2.output.XMLOutputter;

import br.com.housepi.*;
import br.com.housepi.classes.Conexao;
import br.com.housepi.classes.Funcoes;
import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.view.ContextMenu;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.view.ContextMenu.ContextMenuInfo;
import android.view.View.OnClickListener;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.Toast;

public class ConfiguracaoRFID extends Fragment implements OnClickListener {

	private Button btAdicionarRFID;
	private ListView lvRFID;
	private EditText etRFID;
	private String[] menuItems = new String[] {"Remover"};
	private List<String> RFID = new ArrayList<String>();
	private ArrayAdapter<String> arrayAdapter;

		
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,	Bundle savedInstanceState) {

		View rootView = inflater.inflate(R.layout.configuracao_rfid, container, false);
	
		etRFID = (EditText) rootView.findViewById(R.id.etRFID);
		
		btAdicionarRFID = (Button) rootView.findViewById(R.id.btAdicionarRFID);
		btAdicionarRFID.setOnClickListener(this);
		
		lvRFID = (ListView) rootView.findViewById(R.id.lvRFID);
		arrayAdapter = new ArrayAdapter<String>(getActivity(), android.R.layout.simple_list_item_1, RFID);
		lvRFID.setAdapter(arrayAdapter);
		registerForContextMenu(lvRFID);
		
		carregarRFID();
		
		return rootView;
	}
	
	@Override
	public void onCreateContextMenu(ContextMenu menu, View v, ContextMenuInfo menuInfo) {
		if (v.getId() == R.id.lvRFID) {
			menu.setHeaderTitle("O que deseja fazer?");
	    
			for (int i = 0; i < menuItems.length; i++) {
				menu.add(Menu.NONE, i, i, menuItems[i]);
			}
		}
	}

	@Override
	public void onClick(View v) {
		if (v == btAdicionarRFID) {
			if (etRFID.getText().toString().trim().equals("")) {
				Funcoes.msgDialogoInformacao("Atenção", "Informe o número da TAG RFID", this.getActivity());
			} else {
				if (RFID.contains(etRFID.getText().toString().trim())) {
					Funcoes.msgDialogoInformacao("Atenção", "TAG já cadastrada!", this.getActivity());					
				} else {
					if (enviarComando("Adicionar", etRFID.getText().toString().trim())) {
						Toast.makeText(this.getActivity(), "Registro adicionado com sucesso!", Toast.LENGTH_LONG).show();
						RFID.add(etRFID.getText().toString().trim());
						arrayAdapter.notifyDataSetChanged();
						etRFID.setText("");
					} else {
						Toast.makeText(this.getActivity(), "Não foi possível adicionar o registro!", Toast.LENGTH_LONG).show();
					}
				}	
			}
		}
	}
	
	@Override
	public boolean onContextItemSelected(MenuItem item) {
		AdapterView.AdapterContextMenuInfo info = (AdapterView.AdapterContextMenuInfo)item.getMenuInfo();
	  
		if (enviarComando("Remover", String.valueOf(RFID.get(info.position)))) {
			Toast.makeText(this.getActivity(), "Registro removido com sucesso!", Toast.LENGTH_LONG).show();
			RFID.remove(info.position);
			arrayAdapter.notifyDataSetChanged();
		} else {
			Toast.makeText(this.getActivity(), "Não foi possível remover o registro.", Toast.LENGTH_LONG).show();
		}
				  
	  return true;
	}
	
	private boolean enviarComando(String comando, String valor) {
		Document doc = new Document();
		Element root = new Element("ConfiguracaoRFID");
			
		root.addContent(new Element("Comando").setText(comando));
		root.addContent(new Element("Valor").setText(valor));
		
		doc.setRootElement(root);

		Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));
		
		if (Conexao.receberRetornoStatic().equals("Ok")) {
			return true;
		} else {
			return false;
		}
	}
	
	private void carregarRFID() {
		Document doc = new Document();
		String mensagem = "";
		
		Element root = new Element("EnviarRFID");
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
		
		RFID.clear();
		
		if (retorno.getName().equals("EnviarRFID")) {
			@SuppressWarnings("rawtypes")
			List elements = retorno.getChildren();
			@SuppressWarnings("rawtypes")
			Iterator j = elements.iterator();
	
			while (j.hasNext()) {
				Element element = (Element) j.next();
				RFID.add(element.getAttribute("Tag").getValue());
			}
		}
			
		arrayAdapter.notifyDataSetChanged();
	}
}
