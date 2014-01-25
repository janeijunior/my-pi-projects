package br.com.housepi.classes;

import java.io.IOException;
import java.io.Reader;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.Date;
import java.util.Iterator;
import java.util.List;

import org.jdom2.DataConversionException;
import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.JDOMException;
import org.jdom2.input.SAXBuilder;
import org.jdom2.output.XMLOutputter;

public class Agendamento {
	private Integer codigo;
	private String nome;
	private Date dataHoraInicial;
	private Date dataHoraFinal;
	private String diasDaSemana;
	private String equipamentos;
	private String nomeEquipamentos;
	
	public Agendamento() {
		super();
	}
		
	public Agendamento(String nome, Date dataHoraInicial, Date dataHoraFinal) {
		super();
		this.nome = nome;
		this.dataHoraInicial = dataHoraInicial;
		this.dataHoraFinal = dataHoraFinal;
	}
	
	public Integer getCodigo() {
		return codigo;
	}

	public void setCodigo(Integer codigo) {
		this.codigo = codigo;
	}

	public String getNome() {
		return nome;
	}
	public void setNome(String nome) {
		this.nome = nome;
	}
	public Date getDataHoraInicial() {
		return dataHoraInicial;
	}
	public void setDataHoraInicial(Date dataHoraInicial) {
		this.dataHoraInicial = dataHoraInicial;
	}
	public Date getDataHoraFinal() {
		return dataHoraFinal;
	}
	public void setDataHoraFinal(Date dataHoraFinal) {
		this.dataHoraFinal = dataHoraFinal;
	}

	public String getDiasDaSemana() {
		if (this.diasDaSemana.equals("")) {
			return " ";
		} else {
			return diasDaSemana;
		}
	}

	public void setDiasDaSemana(String diasDaSemana) {
		this.diasDaSemana = diasDaSemana;
	}
	
	public String getEquipamentos() {
		return equipamentos;
	}

	public void setEquipamentos(String equipamentos) {
		this.equipamentos = equipamentos;
	}

	public String getNomeEquipamentos() {
		return nomeEquipamentos;
	}

	public void setNomeEquipamentos(String nomeEquipamentos) {
		this.nomeEquipamentos = nomeEquipamentos;
	}

	public Boolean gravarAgendamento() {
		Document doc = new Document();
		Element root = new Element("GravarAgendamento");
		       
		root.addContent(new Element("Nome").setText(this.getNome()));
		root.addContent(new Element("DataHoraInicial").setText(Funcoes.formatarDataHoraBanco(this.getDataHoraInicial())));
		root.addContent(new Element("DataHoraFinal").setText(Funcoes.formatarDataHoraBanco(this.getDataHoraFinal())));
		root.addContent(new Element("Dias").setText(this.getDiasDaSemana()));
		root.addContent(new Element("Equipamentos").setText(this.getEquipamentos()));
		
		doc.setRootElement(root);
		Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));		
			
		if (Conexao.getConexaoAtual().receberRetorno().equals("Ok")) {
			return true;
		} else {
			return false;
		}
	}
	
	public Boolean removerAgendamento() {
		Document doc = new Document();
		Element root = new Element("RemoverAgendamento");
		       
		root.addContent(new Element("Id").setText(this.getCodigo().toString()));
		
		doc.setRootElement(root);
		Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));		
		
		if (Conexao.getConexaoAtual().receberRetorno().equals("Ok")) {
			return true;
		} else {
			return false;
		}	
	}
	
	public static List<Agendamento> getAgendamentos(){
		List<Agendamento> lista = new ArrayList<Agendamento>();
		String mensagem = "";

		try {
			Document doc = new Document();
			
			Element root = new Element("EnviarAgendamento");
			doc.setRootElement(root);

			Conexao.getConexaoAtual().enviarMensagem(new XMLOutputter().outputString(doc));

			mensagem = Conexao.getConexaoAtual().receberRetorno();
						
			SAXBuilder builder = new SAXBuilder();
			Reader in = new StringReader(mensagem);
	
			try {
				doc = builder.build(in);
			} catch (JDOMException e) {
				e.printStackTrace();
			}
	
			Element retorno = (Element) doc.getRootElement();
			
			if (!retorno.getName().equals("EnviarAgendamento")) {
				return lista;
			}
			
			@SuppressWarnings("rawtypes")
			List elements = retorno.getChildren();
			@SuppressWarnings("rawtypes")
			Iterator j = elements.iterator();
	
			Agendamento agendamento;
			
			while (j.hasNext()) {
				Element element = (Element) j.next();
		
				agendamento = new Agendamento();
				
				try {
					agendamento.setCodigo(element.getAttribute("Id").getIntValue());
				} catch (DataConversionException e1) {
					e1.printStackTrace();
				}
				
				agendamento.setNome(element.getAttribute("Nome").getValue());
				agendamento.setDataHoraInicial(Funcoes.formatarDataHora(element.getAttribute("DataHoraInicial").getValue()));
				agendamento.setDataHoraFinal(Funcoes.formatarDataHora(element.getAttribute("DataHoraFinal").getValue()));
				agendamento.setDiasDaSemana(element.getAttribute("Dias").getValue());
				agendamento.setEquipamentos(element.getAttribute("Equipamentos").getValue());
				agendamento.setNomeEquipamentos(element.getAttribute("NomeEquipamentos").getValue());
				
				lista.add(agendamento);
			}
	
		} catch (IOException e) {
			e.printStackTrace();
		}
		return lista;
	}
	
}
