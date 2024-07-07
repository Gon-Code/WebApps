package programacionweb.tarea4.services;

import programacionweb.tarea4.Comentario;
import programacionweb.tarea4.Repositorios.ComentarioRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class ComentarioService {
    
    private final ComentarioRepository comentarioRepository;

    public ComentarioService(ComentarioRepository comentarioRepository) {
        this.comentarioRepository = comentarioRepository;
    }

    // Método en el servicio para obtener ids de comentarios por id_foto
    public List<Integer> findIdsByIdFoto(Integer idFoto) {
        return comentarioRepository.findIdsByIdFoto(idFoto);
    }

    // Método en el servicio para obtener el nombre por id
    public String findNombreById(Integer id) {
        return comentarioRepository.findNombreById(id);
    }

    // Método en el servicio para obtener el comentario por id
    public String findComentarioById(Integer id) {
        return comentarioRepository.findComentarioById(id);
    }

    // Método en el servicio para obtener la fecha por id
    public LocalDateTime findFechaById(Integer id) {
        return comentarioRepository.findFechaById(id);
    }

    public void guardarComentario(Integer idFoto, String nombre, String comentario, LocalDateTime fecha, Integer productoIdFoto) {
        Comentario nuevoComentario = new Comentario();
        nuevoComentario.setNombre(nombre);
        nuevoComentario.setFecha(fecha);
        nuevoComentario.setComentario(comentario);
        nuevoComentario.setIdFoto(idFoto);
        nuevoComentario.setProductoIdFoto(productoIdFoto);

        comentarioRepository.save(nuevoComentario);
    }

    public long countComentariosByIdFoto(Integer idFoto) {
        return comentarioRepository.countByIdFoto(idFoto);
    }
}
