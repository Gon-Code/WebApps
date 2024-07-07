package programacionweb.tarea4.services;

import programacionweb.tarea4.Foto;
import programacionweb.tarea4.Repositorios.FotoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class FotoService {
    @Autowired
    private FotoRepository fotoRepository;

    public List<String> obtenerUltimos20NombresDeArchivo() {
        return fotoRepository.findLast20Fotos()
                .stream()
                .map(Foto::getNombreArchivo)
                .collect(Collectors.toList());
    }

    public Integer obtenerIdPorNombreArchivo(String nombreArchivo) {
        return fotoRepository.findIdByNombreArchivo(nombreArchivo);
    }

    public String obtenerNombreArchivoPorId(Integer id) {
        return fotoRepository.findById(id)
                .map(Foto::getNombreArchivo)
                .orElse(null); // Manejar caso donde el ID no existe
    }

    public Integer obtenerProductoIdPorIdFoto(Integer idFoto) {
        return fotoRepository.findProductoIdByIdFoto(idFoto);
    }

    public List<Integer> obtenerIdPaginados(Integer offset, Integer pageSize) {
        return fotoRepository.findIdPaginados(offset, pageSize);
    }

    // Método para contar el total de fotos
    public long contarTotalFotos() {
        return fotoRepository.contarTotalFotos();
    }
}
