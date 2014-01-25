package br.com.housepi.activity;

import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.output.XMLOutputter;
import br.com.housepi.R;
import br.com.housepi.classes.Conexao;
import br.com.housepi.classes.Funcoes;
import android.annotation.SuppressLint;
import android.content.Intent;
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

@SuppressLint("InlinedApi")
public class ConfiguracaoGeral extends Fragment implements OnClickListener {
	private EditText edtUsuario;
	private EditText edtSenha;
	private CheckBox cbxMostrarSenha;
	private CheckBox cbxAvancado;
	private Button btnSalvar;
	private Button btnReiniciar;
	private Button btnDesligar;
	
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {

		View rootView = inflater.inflate(R.layout.configuracao_geral, container, false);

		edtUsuario = (EditText) rootView.findViewById(R.id.edtUsuarioConf);
		edtSenha = (EditText) rootView.findViewById(R.id.edtSenhaConf);
		
		cbxMostrarSenha = (CheckBox) rootView.findViewById(R.id.cbxMostrarSenhaConf);
		cbxMostrarSenha.setOnClickListener(this);
		
		cbxAvancado = (CheckBox) rootView.findViewById(R.id.cbxAvancado);
		cbxAvancado.setOnClickListener(this);
		
		btnSalvar = (Button) rootView.findViewById(R.id.btnSalvarConfGeral);
		btnSalvar.setOnClickListener(this);
		
		btnReiniciar = (Button) rootView.findViewById(R.id.btnReiniciar);
		btnReiniciar.setOnClickListener(this);
		
		btnDesligar = (Button) rootView.findViewById(R.id.btnDesligar);
		btnDesligar.setOnClickListener(this);
		
		edtUsuario.setText(Funcoes.carregarDadosComponente("edtUsuario", edtUsuario.getText().toString(), this.getActivity()));
		edtSenha.setText(Funcoes.carregarDadosComponente("edtSenha", edtSenha.getText().toString(), this.getActivity()));
	
		controlarBotaoAvancado();
		
		return rootView;
	}
	
	@Override
	public void onResume() {
		if (cbxMostrarSenha.isChecked()) {
			edtSenha.setInputType(InputType.TYPE_CLASS_TEXT);
		} else {
			edtSenha.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD);	
		}
		
		super.onResume();
	}
	
	@Override
	public void onPause() {
		cbxMostrarSenha.setChecked(false);
		cbxAvancado.setChecked(false);

		super.onPause();
	}
	
	
	@Override
    public void onClick(View v) {
		if (v == cbxMostrarSenha) {
			if (cbxMostrarSenha.isChecked()) {
				edtSenha.setInputType(InputType.TYPE_CLASS_TEXT);
			} else {
				edtSenha.setInputType(InputType.TYPE_CLASS_TEXT | InputType.TYPE_TEXT_VARIATION_PASSWORD);	
			}
		} else if (v == cbxAvancado) {
			controlarBotaoAvancado();
		} else if (v == btnReiniciar) {
			reiniciarDesligarServidor("Reiniciar");
		} else if (v == btnDesligar) {
			reiniciarDesligarServidor("Desligar");
		} else if (v == btnSalvar) {
			if (edtUsuario.getText().toString().trim().equals("")) {
				Funcoes.msgDialogoInformacao("Atenção", "Informe o novo usuário.", this.getActivity());
			} else if (edtSenha.getText().toString().trim().equals("")) {
				Funcoes.msgDialogoInformacao("Atenção", "Informe a nova senha.", this.getActivity());
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
				
				mensagem = Conexao.getConexaoAtual().receberRetorno();
				
				if (mensagem.equals("Ok")) {
					Funcoes.msgToastDadosGravados(this.getActivity());
				} else {
					Funcoes.msgToastErroGravar(this.getActivity());
				}
			}
		}
	}
	
	private void reiniciarDesligarServidor(String comando){
		Document doc = new Document();
		Element root = new Element("ReiniciarDesligar");
		       
		Element acao = new Element("Acao");
		acao.setText(comando);
		root.addContent(acao);
		
		doc.setRootElement(root);
		
		Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));
		
		if (Conexao.receberRetornoStatic().equals("Ok")) {
			Intent i = this.getActivity().getBaseContext().getPackageManager().getLaunchIntentForPackage(this.getActivity().getBaseContext().getPackageName());
			i.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
			i.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK);
			startActivity(i);		
		} else {
			Funcoes.msgToastErroComando(this.getActivity());
		}
	}
	
	private void controlarBotaoAvancado() {
		if (cbxAvancado.isChecked()) {
			btnReiniciar.setVisibility(View.VISIBLE);
			btnDesligar.setVisibility(View.VISIBLE);
		} else {
			btnReiniciar.setVisibility(View.GONE);
			btnDesligar.setVisibility(View.GONE);
		}
	}

}
