package programacionweb.tarea4.Repositorios;


import java.time.LocalDateTime;
import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import programacionweb.tarea4.Comentario;

@Repository
public interface ComentarioRepository extends JpaRepository<Comentario, Integer> {
    
    // Método para buscar ids de comentarios por id_foto
    @Query("SELECT c.id FROM Comentario c WHERE c.id_foto = :idFoto ORDER BY c.id DESC")
    List<Integer> findIdsByIdFoto(@Param("idFoto") Integer idFoto);

    // Método para buscar nombre por id
    @Query("SELECT c.nombre FROM Comentario c WHERE c.id = :id")
    String findNombreById(@Param("id") Integer id);

    // Método para buscar comentario por id
    @Query("SELECT c.comentario FROM Comentario c WHERE c.id = :id")
    String findComentarioById(@Param("id") Integer id);

    // Método para buscar fecha por id
    @Query("SELECT c.fecha FROM Comentario c WHERE c.id = :id")
    LocalDateTime findFechaById(@Param("id") Integer id);

    // Método para contar comentarios por id_foto
    @Query("SELECT COUNT(c) FROM Comentario c WHERE c.id_foto = :idFoto")
    long countByIdFoto(@Param("idFoto") Integer idFoto);
}

