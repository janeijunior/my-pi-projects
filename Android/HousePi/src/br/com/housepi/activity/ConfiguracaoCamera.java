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

public class ConfiguracaoCamera extends Fragment implements OnClickListener {
		
		private Button btAdicionarCamera;
		private ListView lvCamera;
		private EditText etNome;
		private EditText etDevice;
		private EditText etPorta;
		private String[] menuItems = new String[] {"Remover"};
		private List<String> Camera = new ArrayList<String>();
		private ArrayAdapter<String> arrayAdapter;
		
		@Override
		public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {

			View rootView = inflater.inflate(R.layout.configuracao_camera, container, false);
			
			etNome = (EditText) rootView.findViewById(R.id.etNomeCamera);
			etDevice = (EditText) rootView.findViewById(R.id.etDevice);
			etPorta = (EditText) rootView.findViewById(R.id.etPortaCamera);
			
			btAdicionarCamera = (Button) rootView.findViewById(R.id.btAdicionarCamera);
			btAdicionarCamera.setOnClickListener(this);
			
			lvCamera = (ListView) rootView.findViewById(R.id.lvCamera);
			arrayAdapter = new ArrayAdapter<String>(getActivity(), android.R.layout.simple_list_item_1, Camera);
			lvCamera.setAdapter(arrayAdapter);
			registerForContextMenu(lvCamera);
			
			carregarCamera();
		
			return rootView;
		}
		
		@Override
		public void onCreateContextMenu(ContextMenu menu, View v, ContextMenuInfo menuInfo) {
			if (v.getId() == R.id.lvCamera) {
				menu.setHeaderTitle("O que deseja fazer?");
		    
				for (int i = 0; i < menuItems.length; i++) {
					menu.add(Menu.NONE, i, i, menuItems[i]);
				}
			}
		}

		@Override
		public void onClick(View v) {
			if (v == btAdicionarCamera) {
				if ((etNome.getText().toString().trim().equals("")) || (etDevice.getText().toString().trim().equals("")) || (etPorta.getText().toString().trim().equals(""))) {
					Funcoes.msgDialogoInformacao("Atenção", "Preencha todos os campos antes de continuar!", this.getActivity());
				} else {
					if (Camera.contains(etNome.getText().toString().trim())) {
						Funcoes.msgDialogoInformacao("Atenção", "Já existe uma câmera com este nome. Verifique!", this.getActivity());					
					} else {
						if (enviarComando("Adicionar", "")) {
							Toast.makeText(this.getActivity(), "Registro adicionado com sucesso!", Toast.LENGTH_LONG).show();
							Camera.add(etNome.getText().toString().trim());
							arrayAdapter.notifyDataSetChanged();
							etNome.setText("");
							etDevice.setText("");
							etPorta.setText("");
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
		  
			if (enviarComando("Remover", String.valueOf(Camera.get(info.position)))) {
				Toast.makeText(this.getActivity(), "Registro removido com sucesso!", Toast.LENGTH_LONG).show();
				Camera.remove(info.position);
				arrayAdapter.notifyDataSetChanged();
			} else {
				Toast.makeText(this.getActivity(), "Não foi possível remover o registro.", Toast.LENGTH_LONG).show();
			}
					  
		  return true;
		}
		
		private boolean enviarComando(String comando, String valor) {
			Document doc = new Document();
			Element root = new Element("ConfiguracaoCamera");
				
			if (comando.equals("Adicionar")) {
				root.addContent(new Element("Comando").setText(comando));
				root.addContent(new Element("Nome").setText(etNome.getText().toString().trim()));
				root.addContent(new Element("Device").setText(etDevice.getText().toString().trim()));
				root.addContent(new Element("Porta").setText(etPorta.getText().toString().trim()));
			} else {
				root.addContent(new Element("Comando").setText(comando));
				root.addContent(new Element("Nome").setText(valor));
			}
			
			doc.setRootElement(root);
			Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));
			
			if (Conexao.receberRetornoStatic().equals("Ok")) {
				return true;
			} else {
				return false;
			}
		}
		
		private void carregarCamera() {
			Document doc = new Document();
			String mensagem = "";
			
			Element root = new Element("EnviarCamera");
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
			
			Camera.clear();
			
			if (retorno.getName().equals("EnviarCamera")) {
				@SuppressWarnings("rawtypes")
				List elements = retorno.getChildren();
				@SuppressWarnings("rawtypes")
				Iterator j = elements.iterator();
		
				while (j.hasNext()) {
					Element element = (Element) j.next();
					Camera.add(element.getAttribute("Nome").getValue());
				}
			}
				
			arrayAdapter.notifyDataSetChanged();
		}
	}
