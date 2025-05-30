from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from db import get_db_connection
import traceback

feedbacks_bp = Blueprint('feedbacks', __name__)


@feedbacks_bp.route('/feedbacks', methods=["POST", "GET"])
def feedbacks():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":
        try:
            nota = request.form["nota"]
            comentario = request.form["comentario"]
            usuario_id = request.form["usuario_id"]
            unidade_id = request.form["unidade_id"]

            elogios = request.form.getlist("elogios[]")
            motivos = request.form.getlist("motivos[]")

            opcoes_selecionadas = elogios + motivos
            outro = ", ".join(
                opcoes_selecionadas) if opcoes_selecionadas else None

            print(
                f"Nota: {nota}, Comentário: {comentario}, Outro: {outro}, Usuario ID: {usuario_id}, Unidade ID: {unidade_id}"
            )

            cursor.execute("""
                INSERT INTO feedback (nota_user, Comentario, id_user_feedback, id_unidade, Outro)
                VALUES (%s, %s, %s, %s, %s)
            """, (nota, comentario, usuario_id, unidade_id, outro))
            connection.commit()

            flash("Feedback enviado com sucesso!", "success")
            return redirect(url_for('feedbacks.feedbacks'))

        except Exception as e:
            connection.rollback()
            print(f"Erro ao salvar feedback: {e}")
            flash("Erro ao enviar feedback.", "error")
            return f"Erro ao salvar no banco: {e}", 500

        finally:
            cursor.close()
            connection.close()

    else:
        try:
            cursor.execute("""
                SELECT ID_Unidades, Nome_Unidade FROM unidades
            """)
            unidades = cursor.fetchall()

        except Exception as e:
            print(f"Erro ao buscar unidades: {e}")
            return f"Erro ao buscar unidades: {e}", 500

        finally:
            cursor.close()
            connection.close()

        return render_template("feedbacks.html", unidades=unidades)


@feedbacks_bp.route('/relatorios', methods=["GET"])
def relatorios():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            (SUM(CASE WHEN nota_user = 5 THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS `5 estrelas`,
            (SUM(CASE WHEN nota_user = 4 THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS `4 estrelas`,
            (SUM(CASE WHEN nota_user = 3 THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS `3 estrelas`,
            (SUM(CASE WHEN nota_user = 2 THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS `2 estrelas`,
            (SUM(CASE WHEN nota_user = 1 THEN 1 ELSE 0 END) / COUNT(*)) * 100 AS `1 estrela`
        FROM feedback
    """)
    porcentagens = cursor.fetchone()

    cursor.execute("""
         SELECT 
        f.nota_user,
        f.Comentario,
        f.id_user_feedback,
        u.Nome_Unidade AS nome_unidade,
        r.Nome_Regiao AS nome_regiao
        FROM feedback f
        LEFT JOIN unidades u ON f.id_unidade = u.ID_Unidades
        LEFT JOIN regiao r ON u.ID_Regiao = r.ID_Regiao
        WHERE f.Comentario IS NOT NULL AND f.Comentario != ''
        ORDER BY f.nota_user;
    """)
    comentarios = cursor.fetchall()

    cursor.close()
    conn.close()
    print(type(comentarios))
    return render_template('relatorios.html',
                           porcentagens=porcentagens,
                           comentarios=comentarios)


@feedbacks_bp.route("/api/feedback_porcentagem/<id_unidade>")
def feedback_porcentagem(id_unidade):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Permitir 'todas' ou 0 para buscar geral
        if str(id_unidade) == 'todas' or str(id_unidade) == '0':
            cursor.execute("""
                SELECT
                    SUM(CASE WHEN nota_user = 5 THEN 1 ELSE 0 END) AS cinco,
                    SUM(CASE WHEN nota_user = 4 THEN 1 ELSE 0 END) AS quatro,
                    SUM(CASE WHEN nota_user = 3 THEN 1 ELSE 0 END) AS tres,
                    SUM(CASE WHEN nota_user = 2 THEN 1 ELSE 0 END) AS dois,
                    SUM(CASE WHEN nota_user = 1 THEN 1 ELSE 0 END) AS um,
                    COUNT(*) AS total
                FROM feedback
                WHERE nota_user BETWEEN 1 AND 5
            """)
            row = cursor.fetchone()
        else:
            cursor.execute("""
                SELECT
                    SUM(CASE WHEN nota_user = 5 THEN 1 ELSE 0 END) AS cinco,
                    SUM(CASE WHEN nota_user = 4 THEN 1 ELSE 0 END) AS quatro,
                    SUM(CASE WHEN nota_user = 3 THEN 1 ELSE 0 END) AS tres,
                    SUM(CASE WHEN nota_user = 2 THEN 1 ELSE 0 END) AS dois,
                    SUM(CASE WHEN nota_user = 1 THEN 1 ELSE 0 END) AS um,
                    COUNT(*) AS total
                FROM feedback
                WHERE id_unidade = %s AND nota_user BETWEEN 1 AND 5
            """, (id_unidade,))
            row = cursor.fetchone()

        total = row["total"] or 1

        porcentagens = {
            "5 estrelas": round((row["cinco"] / total) * 100, 1),
            "4 estrelas": round((row["quatro"] / total) * 100, 1),
            "3 estrelas": round((row["tres"] / total) * 100, 1),
            "2 estrelas": round((row["dois"] / total) * 100, 1),
            "1 estrela": round((row["um"] / total) * 100, 1),
            "total_5": row["cinco"] or 0,
            "total_4": row["quatro"] or 0,
            "total_3": row["tres"] or 0,
            "total_2": row["dois"] or 0,
            "total_1": row["um"] or 0
        }

        return jsonify(porcentagens)

    except Exception as e:
        print("Erro ao consultar dados:")
        traceback.print_exc()
        return jsonify({"erro": "Erro ao consultar dados"}), 500

    finally:
        cursor.close()
        conn.close()


@feedbacks_bp.route("/feedbackstar")
def feedbackstar():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT ID_Unidades, Nome_Unidade FROM unidades")
        unidades = cursor.fetchall()
        return render_template("feedbackstar.html", unidades=unidades)

    except Exception as e:
        print("Erro ao carregar unidades:", e)
        return "Erro ao carregar página", 500

    finally:
        cursor.close()
        conn.close()


@feedbacks_bp.route("/api/feedback_comentarios/<id_unidade>")
def feedback_comentarios(id_unidade):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        nota = request.args.get('nota')
        usuario = request.args.get('usuario')
        limit = int(request.args.get('limit', 10))
        page = int(request.args.get('page', 1))
        offset = (page - 1) * limit
        params = []
        if str(id_unidade) == 'todas' or str(id_unidade) == '0':
            query_base = '''
                FROM feedback f
                LEFT JOIN unidades u ON f.id_unidade = u.ID_Unidades
                LEFT JOIN usuario usr ON f.id_user_feedback = usr.ID_User
                WHERE f.Comentario IS NOT NULL AND f.Comentario != ''
            '''
        else:
            query_base = '''
                FROM feedback f
                LEFT JOIN unidades u ON f.id_unidade = u.ID_Unidades
                LEFT JOIN usuario usr ON f.id_user_feedback = usr.ID_User
                WHERE f.id_unidade = %s AND f.Comentario IS NOT NULL AND f.Comentario != ''
            '''
            params.append(id_unidade)
        if nota:
            query_base += ' AND f.nota_user = %s'
            params.append(nota)
        if usuario:
            query_base += ' AND usr.Nome_User LIKE %s'
            params.append(f"%{usuario}%")
        # Total
        cursor.execute(f"SELECT COUNT(*) as total {query_base}", params)
        total = cursor.fetchone()['total']
        # Comentários paginados
        query = f'''
            SELECT f.nota_user, f.Comentario, f.id_user_feedback, u.Nome_Unidade AS nome_unidade, usr.Nome_User AS nome_usuario
            {query_base}
            ORDER BY f.nota_user DESC, f.idfeedback DESC
            LIMIT %s OFFSET %s
        '''
        params_paged = params + [limit, offset]
        cursor.execute(query, params_paged)
        comentarios = cursor.fetchall()
        return jsonify({"comentarios": comentarios, "total": total})
    except Exception as e:
        print("Erro ao consultar comentários:", e)
        return jsonify({"erro": "Erro ao consultar comentários"}), 500
    finally:
        cursor.close()
        conn.close()
