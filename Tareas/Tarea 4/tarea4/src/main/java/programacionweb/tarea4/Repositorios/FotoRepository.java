package programacionweb.tarea4.Repositorios;


import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import programacionweb.tarea4.Foto;

import java.util.List;

@Repository
public interface FotoRepository extends JpaRepository<Foto, Integer> {
    
    @Query(value = "SELECT * FROM foto ORDER BY id DESC LIMIT 20", nativeQuery = true)
    List<Foto> findLast20Fotos();

    @Query("SELECT f.id FROM Foto f WHERE f.nombreArchivo = :nombreArchivo")
    Integer findIdByNombreArchivo(String nombreArchivo);

    @Query("SELECT f.productoId FROM Foto f WHERE f.id = :idFoto")
    Integer findProductoIdByIdFoto(@Param("idFoto") Integer idFoto);
    
    @Query(value = "SELECT id FROM foto ORDER BY id DESC LIMIT :offset, :pageSize", nativeQuery = true)
    List<Integer> findIdPaginados(@Param("offset") Integer offset, @Param("pageSize") Integer pageSize);

    // Método para contar el total de fotos
    @Query("SELECT COUNT(f) FROM Foto f")
    long contarTotalFotos();
}

