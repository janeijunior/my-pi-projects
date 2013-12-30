package br.com.housepi.activity;

import java.io.IOException;
import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.output.XMLOutputter;
import br.com.housepi.R;
import br.com.housepi.classes.Conexao;
import br.com.housepi.classes.Funcoes;
import android.os.Bundle;
import android.support.v4.app.Fragment;
import android.text.InputType;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;

public class ConfiguracaoGeral extends Fragment implements OnClickListener {
	private EditText edtUsuario;
	private EditText edtSenha;
	private CheckBox cbxMostrarSenha;
	private Button btnSalvar;
	
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {

		View rootView = inflater.inflate(R.layout.configuracao_geral, container, false);

		edtUsuario = (EditText) rootView.findViewById(R.id.edtUsuarioConf);
		edtSenha = (EditText) rootView.findViewById(R.id.edtSenhaConf);
		
		cbxMostrarSenha = (CheckBox) rootView.findViewById(R.id.cbxMostrarSenhaConf);
		cbxMostrarSenha.setOnClickListener(this);
		
		btnSalvar = (Button) rootView.findViewById(R.id.btnSalvarConfGeral);
		btnSalvar.setOnClickListener(this);
		
		edtUsuario.setText(Funcoes.carregarDadosComponente("edtUsuario", edtUsuario.getText().toString(), this.getActivity()));
		edtSenha.setText(Funcoes.carregarDadosComponente("edtSenha", edtSenha.getText().toString(), this.getActivity()));
	
		return rootView;
	}
	
	@SuppressWarnings("deprecation")
	@Override
    public void onClick(View view) {
		if (view == cbxMostrarSenha) {
			if (cbxMostrarSenha.isChecked()) {
				edtSenha.setInputType(InputType.TYPE_CLASS_TEXT);
			} else {
				edtSenha.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD);	
			}
		} else if (view == btnSalvar) {
			if (edtUsuario.getText().toString().trim().equals("")) {
				Funcoes.exibirDialogoInformacao("Atenção", "Informe o novo usuário.", this.getActivity());
			} else if (edtSenha.getText().toString().trim().equals("")) {
				Funcoes.exibirDialogoInformacao("Atenção", "Informe a nova senha.", this.getActivity());
			} else {
				String mensagem = "";
				
				Document doc = new Document();
				Element root = new Element("AlterarUsuarioSenha");
				         
				Element usuario = new Element("Usuario");
				usuario.setText(edtUsuario.getText().toString());
				root.addContent(usuario);
				
				Element senha = new Element("Senha");
				senha.setText(edtSenha.getText().toString());
				root.addContent(senha);
				
				doc.setRootElement(root);
				
				mensagem = new XMLOutputter().outputString(doc);				
				Conexao.getConexaoAtual().enviarMensagem(mensagem);
				
				try {
					mensagem = Conexao.getConexaoAtual().getIn().readLine();
					
					if (mensagem.equals("Ok")) {
						Funcoes.msgToastDadosGravados(this.getActivity());
					} else {
						Funcoes.msgToastErroGravar(this.getActivity());
					}
				} catch (IOException e) {
					Funcoes.msgToastErroGravar(this.getActivity());
				} 
			}
		}
	}

}
