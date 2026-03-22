$(".excluir").click(function(){
    $('#ExcluirProjeto').modal('show');
    id = $(this).attr('id');
    nome = $(this).attr('name');
    $('.projeto').html(nome);
    $(".confirmar_exclusao").off('click').on('click', function(e){ // Preserve other event handlers if any.
        $('.redirect').attr('href', '/projetos/'+valor+'/excluir')
    });
  });