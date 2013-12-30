package br.com.housepi.classes;

import java.io.IOException;
import java.io.Reader;
import java.io.StringReader;
import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.JDOMException;
import org.jdom2.input.SAXBuilder;
import org.jdom2.output.XMLOutputter;

import android.widget.ToggleButton;

public class Alarme {
	private Boolean alarmeLigado;
	private Boolean panicoLigado;
	private ToggleButton btnAlarme;
	private ToggleButton btnPanico;
	
	public Alarme() {
		super();
		
	}
	
	public Alarme(ToggleButton btnAlarme, ToggleButton btnPanico) {
		super();
		this.btnAlarme = btnAlarme;
		this.btnPanico = btnPanico;
	}

	public ToggleButton getBtnAlarme() {
		return btnAlarme;
	}

	public void setBtnAlarme(ToggleButton btnAlarme) {
		this.btnAlarme = btnAlarme;
	}

	public ToggleButton getBtnPanico() {
		return btnPanico;
	}

	public void setBtnPanico(ToggleButton btnPanico) {
		this.btnPanico = btnPanico;
	}
	
	public Boolean getAlarmeLigado() {
		return alarmeLigado;
	}

	public void setAlarmeLigado(Boolean alarmeLigado) {
		this.alarmeLigado = alarmeLigado;
	}

	public Boolean getPanicoLigado() {
		return panicoLigado;
	}

	public void setPanicoLigado(Boolean panicoLigado) {
		this.panicoLigado = panicoLigado;
	}

	public Boolean ligarAlarme() {
		return montarEnviarXMLControle("Alarme", "Ligar");	
	}
	
	public Boolean desligarAlarme() {
		return montarEnviarXMLControle("Alarme", "Desligar");
	}
	
	public Boolean ligarPanico() {
		return montarEnviarXMLControle("Panico", "Ligar");
	}
	
	public Boolean desligarPanico() {
		return montarEnviarXMLControle("Panico", "Desligar");
	}
	
	@SuppressWarnings("deprecation")
	private Boolean montarEnviarXMLControle(String funcao, String comando) {
		Document doc = new Document();
		Element root = new Element(funcao);
		       
		Element acao = new Element("Acao");	
		
		acao.setText(comando);
		
		root.addContent(acao);
		doc.setRootElement(root);
		Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));
		
		try {
			if (Conexao.getConexaoAtual().getIn().readLine().equals("Ok")) {
				return true;
			} else {
				return false;
			}
		} catch (IOException e) {
			e.printStackTrace();
			return false;
		}
	}
	
	@SuppressWarnings("deprecation")
	public void getConfiguracaoStatus() {
		try {
			Document doc = new Document();
			Element root = new Element("StatusAlarme");
			doc.setRootElement(root);

			Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));

			String mensagem = "";

			mensagem = Conexao.getConexaoAtual().getIn().readLine();

			SAXBuilder builder = new SAXBuilder();
			Reader in = new StringReader(mensagem);

			try {
				doc = builder.build(in);
			} catch (JDOMException e) {
				e.printStackTrace();
			}

			Element retorno = (Element) doc.getRootElement();
			
			this.setAlarmeLigado(retorno.getChild("SensorAlarme").getAttribute("Ligado").getIntValue() == 1);
			this.getBtnAlarme().setChecked(this.getAlarmeLigado());
			
			this.setPanicoLigado(retorno.getChild("PanicoAlarme").getAttribute("Ligado").getIntValue() == 1);
			this.getBtnPanico().setChecked(this.getPanicoLigado());
			
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

}
