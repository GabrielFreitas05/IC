from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, 
    QAbstractItemView, QFileDialog
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from db.db import conectar
from telas.tela_processos import TelaProcessos
from fpdf import FPDF

class TelaGerenciarProcessos(QWidget):
    def __init__(self, usuario_id):
        super().__init__()
        self.usuario_id = usuario_id
        self.setWindowTitle("Gerenciamento de Processos")
        self.setFixedSize(1000, 800)
        self.setStyleSheet("""
            QWidget {
                background-color: #1B3A5E;
                color: white;
                font-family: 'Segoe UI';
            }
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #FFCD00;
            }
            QPushButton {
                background-color: #FFCD00;
                color: #1B3A5E;
                font-weight: bold;
                border: none;
                padding: 12px;
                border-radius: 6px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #e6b800;
            }
            QPushButton:disabled {
                background-color: #555555;
                color: #aaaaaa;
            }
            QTableWidget {
                background-color: white;
                color: black;
                border-radius: 8px;
                font-size: 11pt;
                selection-background-color: #FFCD00;
            }
            QHeaderView::section {
                background-color: #1A2A47;
                color: #FFCD00;
                padding: 8px;
                font-weight: bold;
                font-size: 11pt;
            }
            QTableWidget::item:selected {
                background-color: #FFCD00;
                color: #1B3A5E;
            }
        """)
        self._setup_ui()
        self._carregar_processos()

    def _setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        title_label = QLabel("Gerenciamento de Processos")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont('Segoe UI', 20))
        main_layout.addWidget(title_label)

        button_layout = QHBoxLayout()
        
        self.btn_criar = QPushButton("➕ Criar Novo")
        self.btn_criar.clicked.connect(self._abrir_tela_criar_processo)
        button_layout.addWidget(self.btn_criar)

        self.btn_editar = QPushButton("✏️ Editar")
        self.btn_editar.clicked.connect(self._editar_processo_selecionado)
        self.btn_editar.setEnabled(False)
        button_layout.addWidget(self.btn_editar)

        self.btn_excluir = QPushButton("❌ Excluir")
        self.btn_excluir.clicked.connect(self._excluir_processo_selecionado)
        self.btn_excluir.setEnabled(False)
        button_layout.addWidget(self.btn_excluir)

        self.btn_atualizar = QPushButton("🔄 Atualizar")
        self.btn_atualizar.clicked.connect(self._atualizar_processos)
        button_layout.addWidget(self.btn_atualizar)

        self.btn_gerar_relatorio = QPushButton("📄 Gerar Relatório")
        self.btn_gerar_relatorio.clicked.connect(self._gerar_relatorio_processo)
        self.btn_gerar_relatorio.setEnabled(False)
        button_layout.addWidget(self.btn_gerar_relatorio)

        main_layout.addLayout(button_layout)

        self.tabela_processos = QTableWidget()
        self.tabela_processos.setColumnCount(4)
        self.tabela_processos.setHorizontalHeaderLabels(["ID", "Nome do Processo", "Responsável", "Criado em"])
        self.tabela_processos.verticalHeader().setVisible(False)
        self.tabela_processos.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tabela_processos.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tabela_processos.setAlternatingRowColors(True)
        self.tabela_processos.setColumnHidden(0, True)
        
        header = self.tabela_processos.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        self.tabela_processos.itemSelectionChanged.connect(self._atualizar_botoes)
        main_layout.addWidget(self.tabela_processos)

        self.btn_voltar = QPushButton("← Voltar")
        self.btn_voltar.clicked.connect(self._voltar_tela_usuario)
        main_layout.addWidget(self.btn_voltar, alignment=Qt.AlignmentFlag.AlignRight)

    def _carregar_processos(self):
        self.tabela_processos.setRowCount(0)
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nome_processo, responsavel, strftime('%d/%m/%Y', data_inicio) 
                FROM formularios_processos 
                WHERE usuario_id = ? 
                ORDER BY data_inicio DESC
                """, (self.usuario_id,))
            processos = cursor.fetchall()
            if processos:
                for row_idx, (processo_id, nome, responsavel, data) in enumerate(processos):
                    self.tabela_processos.insertRow(row_idx)
                    self.tabela_processos.setItem(row_idx, 0, QTableWidgetItem(str(processo_id)))
                    self.tabela_processos.setItem(row_idx, 1, QTableWidgetItem(nome))
                    self.tabela_processos.setItem(row_idx, 2, QTableWidgetItem(responsavel))
                    self.tabela_processos.setItem(row_idx, 3, QTableWidgetItem(data))
                    for col in [0, 2, 3]:
                        item = self.tabela_processos.item(row_idx, col)
                        if item: 
                            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao carregar processos:\n{str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def _atualizar_botoes(self):
        selected = len(self.tabela_processos.selectedItems()) > 0
        self.btn_editar.setEnabled(selected)
        self.btn_excluir.setEnabled(selected)
        self.btn_gerar_relatorio.setEnabled(selected)

    def _abrir_tela_criar_processo(self):
        self.tela_processos = TelaProcessos(self.usuario_id)
        self.tela_processos.deve_retornar.connect(self._voltar_da_edicao)
        self.tela_processos.destroyed.connect(self._reexibir_e_recarregar)
        self.tela_processos.show()
        self.hide()

    def _editar_processo_selecionado(self):
        selected_items = self.tabela_processos.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Selecione um processo para editar.")
            return
        try:
            selected_row = selected_items[0].row()
            item_id = self.tabela_processos.item(selected_row, 0)
            processo_id = int(item_id.text())
            self.tela_processos = TelaProcessos(self.usuario_id, processo_id=processo_id)
            self.tela_processos.deve_retornar.connect(self._voltar_da_edicao)
            self.tela_processos.destroyed.connect(self._reexibir_e_recarregar)
            self.tela_processos.show()
            self.hide()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao abrir processo:\n{str(e)}")

    def _voltar_da_edicao(self):
        if hasattr(self, 'tela_processos'):
            self.tela_processos.close()
        self.show()

    def _excluir_processo_selecionado(self):
        selected_items = self.tabela_processos.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Selecione um processo para excluir.")
            return
        try:
            selected_row = selected_items[0].row()
            item_id = self.tabela_processos.item(selected_row, 0)
            processo_id = int(item_id.text())
            nome_processo = self.tabela_processos.item(selected_row, 1).text()
            confirm = QMessageBox.question(
                self, 
                "Confirmar Exclusão",
                f"Tem certeza que deseja excluir o processo:\n\n"
                f"ID: {processo_id}\n"
                f"Nome: {nome_processo}\n\n"
                "Esta ação não pode ser desfeita!",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if confirm == QMessageBox.StandardButton.Yes:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM formularios_processos WHERE id = ?", (processo_id,))
                conn.commit()
                QMessageBox.information(self, "Sucesso", f"Processo {nome_processo} excluído com sucesso!")
                self._carregar_processos()
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao excluir processo:\n{str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()

    def _atualizar_processos(self):
        self._carregar_processos()

    def _reexibir_e_recarregar(self):
        self.show()
        self._carregar_processos()

    def _voltar_tela_usuario(self):
        from telas.tela_usuario import tela_usuario
        self.close()
        tela_usuario(self.usuario_id)

    def _gerar_relatorio_processo(self):
        selected_items = self.tabela_processos.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Selecione um processo para gerar o relatório.")
            return

        try:
            selected_row = selected_items[0].row()
            processo_id = int(self.tabela_processos.item(selected_row, 0).text())

            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM formularios_processos WHERE id = ?", (processo_id,))
            processo_detalhes = cursor.fetchone()
            conn.close()

            if processo_detalhes:
                column_names = [
                    "",
                    "",
                    "Nome do Processo",
                    "Responsável",
                    "Data de Início",
                    "Nome da Fase",
                    "Ordem da Fase",
                    "Objetivo da Fase",
                    "Nome do Passo",
                    "Ordem do Passo",
                    "Descrição do Passo",
                    "Ferramentas",
                    "Tempo Estimado",
                    "Riscos",
                    "Entradas",
                    "Saídas",
                    "Depende",
                    "Depende Qual",
                    "Decisão",
                    "Fluxo de Decisão",
                    "Tempo Real",
                    "Qualidade",
                    "Lições Aprendidas",
                    "Melhorias Sugeridas",
                    "",
                    "Data de Registro"
                ]

                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', size=16)
                
                pdf.cell(0, 10, txt="Relatório de Processo", ln=True, align='C')
                pdf.set_font("Arial", size=12)
                pdf.ln(10)
                
                pdf.set_font("Arial", 'B', size=14)
                pdf.cell(0, 10, txt=f"Processo: {processo_detalhes[2]}", ln=True)
                pdf.set_font("Arial", size=12)
                
                pdf.cell(0, 10, txt=f"Responsável: {processo_detalhes[3]}", ln=True)
                pdf.cell(0, 10, txt=f"Data de Início: {processo_detalhes[4]}", ln=True)
                pdf.ln(10)

                pdf.set_font("Arial", 'B', size=12)
                pdf.cell(0, 10, txt="Detalhes do Processo:", ln=True)
                pdf.set_font("Arial", size=12)
                pdf.ln(5)

                for i, (detail, name) in enumerate(zip(processo_detalhes, column_names)):
                    if i in [0, 1, 24]:
                        continue
                        
                    if name and detail:
                        pdf.set_font("Arial", 'B', size=12)
                        pdf.cell(40, 10, txt=f"{name}: ", ln=0)
                        pdf.set_font("Arial", size=12)
                        pdf.multi_cell(0, 10, txt=str(detail))
                        pdf.ln(2)
                
                file_name = f"Relatorio_Processo_{processo_detalhes[2].replace(' ', '_')}.pdf"
                file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Relatório", file_name, "PDF Files (*.pdf)")

                if file_path:
                    pdf.output(file_path)
                    QMessageBox.information(self, "Sucesso", f"Relatório gerado com sucesso em:\n{file_path}")
                else:
                    QMessageBox.information(self, "Cancelado", "Geração do relatório cancelada.")

            else:
                QMessageBox.warning(self, "Erro", "Detalhes do processo não encontrados para gerar o relatório.")

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Falha ao gerar relatório:\n{str(e)}")
