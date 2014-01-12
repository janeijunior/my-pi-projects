package br.com.housepi.activity;

import java.io.Reader;
import java.io.StringReader;
import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.JDOMException;
import org.jdom2.input.SAXBuilder;
import org.jdom2.output.XMLOutputter;
import br.com.housepi.R;
import br.com.housepi.classes.Conexao;
import br.com.housepi.classes.Funcoes;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;

public class ConfiguracaoEmail extends Fragment implements OnClickListener {
	private Button btnSalvar;
	private EditText edtUsuario;
	private EditText edtSenha;
	private EditText edtDestinatario;
	private EditText edtServidor;
	private EditText edtPorta;	
	
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
		
		View rootView = inflater.inflate(R.layout.configuracao_email, container, false);

		btnSalvar = (Button) rootView.findViewById(R.id.btnSalvarConfEmail);
		btnSalvar.setOnClickListener(this);
		
		edtUsuario = (EditText) rootView.findViewById(R.id.edtUsuarioEmail);
		edtSenha = (EditText) rootView.findViewById(R.id.edtSenhaEmail);
		edtDestinatario = (EditText) rootView.findViewById(R.id.edtDestinatarioEmail);
		edtServidor = (EditText) rootView.findViewById(R.id.edtServidorEmail);
		edtPorta = (EditText) rootView.findViewById(R.id.edtPortaEmail);		
		
		getConfiguracaoAtual();
		
		return rootView;
	}
	
	@Override
	public void onClick(View v) {
		if (v == btnSalvar) {
			if (edtUsuario.getText().toString().trim().equals("") || edtSenha.getText().toString().trim().equals("") ||
				edtDestinatario.getText().toString().trim().equals("") || edtServidor.getText().toString().trim().equals("") ||
				edtPorta.getText().toString().trim().equals("")) {
				Funcoes.msgDialogoInformacao("Atenção", "Preencha todos os campos antes de salvar.", this.getActivity());
			} else {
				String mensagem = "";
				
				Document doc = new Document();
				Element root = new Element("AlterarConfiguracaoEmail");
				         
				root.addContent(new Element("Usuario").setText(edtUsuario.getText().toString()));
				root.addContent(new Element("Senha").setText(edtSenha.getText().toString()));
				root.addContent(new Element("Destinatario").setText(edtDestinatario.getText().toString()));
				root.addContent(new Element("Servidor").setText(edtServidor.getText().toString()));
				root.addContent(new Element("Porta").setText(edtPorta.getText().toString()));
				
				doc.setRootElement(root);
				
				mensagem = new XMLOutputter().outputString(doc);				
				Conexao.getConexaoAtual().enviarMensagem(mensagem);
				
				mensagem = Conexao.getConexaoAtual().receberRetorno();
				
				if (mensagem.equals("Ok")) {
					Funcoes.msgToastDadosGravados(this.getActivity());
				} else {
					Funcoes.msgToastErroGravar(this.getActivity());
				}
			}
		}
	}
	
	public void getConfiguracaoAtual() {
		try {		
			Document doc = new Document();
			Element root = new Element("EnviarConfiguracaoEmail");
			doc.setRootElement(root);
	
			Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));
	
			String mensagem = "";
	
			mensagem = Conexao.getConexaoAtual().receberRetorno();
	
			SAXBuilder builder = new SAXBuilder();
			Reader in = new StringReader(mensagem);
	
			try {
				doc = builder.build(in);
			} catch (JDOMException e) {
				e.printStackTrace();
			}
	
			Element retorno = (Element) doc.getRootElement();
			
			if (!retorno.getName().equals("EnviarConfiguracaoEmail")) {
				Funcoes.msgToastErroComando(this.getActivity());
				return;
			}
			
			edtUsuario.setText(retorno.getChild("Dados").getAttribute("Usuario").getValue());
			edtSenha.setText(retorno.getChild("Dados").getAttribute("Senha").getValue());
			edtDestinatario.setText(retorno.getChild("Dados").getAttribute("Destinatario").getValue());
			edtServidor.setText(retorno.getChild("Dados").getAttribute("Servidor").getValue());
			edtPorta.setText(retorno.getChild("Dados").getAttribute("Porta").getValue());
			
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
