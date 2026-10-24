<?php
/**
 * Portal · Historial médico (consultas, diagnósticos y tratamientos)
 * @var array $p @var array $consultas
 */
$titulo = 'Historial médico';
?>
<div class="page-head">
    <div>
        <div class="eyebrow"><?= icono('historial', 14) ?> Mi salud</div>
        <h1>Mi historial médico</h1>
        <p>Consultas atendidas, diagnósticos y tratamientos indicados por sus médicos.</p>
    </div>
    <button type="button" class="btn btn-outline" onclick="window.print()"><?= icono('imprimir') ?> Imprimir</button>
</div>

<div class="ficha">
    <div class="card anim">
        <div class="card-head"><h2>Resumen</h2></div>
        <div class="kv-list">
            <div><span><?= icono('gota', 16) ?> Sangre</span><span><?= e($p['tiposangre'] ?: '—') ?></span></div>
            <div><span><?= icono('alerta', 16) ?> Alergias</span><span><?= e($p['alergias'] ?: '—') ?></span></div>
            <div><span>Crónicas</span><span><?= e($p['enfermedadescronicas'] ?: '—') ?></span></div>
            <div><span>Medicación</span><span><?= e($p['medicacionhabitual'] ?: '—') ?></span></div>
            <div><span>Consultas</span><span><?= count($consultas) ?></span></div>
        </div>
    </div>
    <div class="card anim">
        <div class="card-head"><h2>Consultas</h2></div>
        <?= View::parcial('consultas', ['consultas' => $consultas]) ?>
    </div>
</div>
