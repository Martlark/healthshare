function PageQuestion(){
    
    function vote(button){
        var id = $(button).data('id');
        var direction = $(button).data('direction');
        var $total_vote = $('#total_vote_'+id);
        var $message = $('#message_vote_'+id);
            
        $.ajax({
            url: '/api/answer/{0}/vote/{1}'.format(id, direction),
            dataType: 'json',
            cache : false
        }).done(function( data ) {
            $message.html("");
            if( data.result && data.result == 'ok'){
                $message.html("");
                $total_vote.html(data.message);
            }else if(data.message){
                $message.html(data.message);
            }else{
                $message.html('api return makes no sense');
            }
        }).fail(function(xhr,errorText){
            $message.html('error:' + errorText + ' - ' + xhr.statusText);
        });
    }
    
    function editQuestion(){
        $('#div_display_question').hide();
        $('#div_edit_question').show();
        $('form[name="submit_answer"]').fadeOut();
    }
    
    this.init = function(){
        
        $('#button_edit_question').click(function(evt){
            evt.preventDefault();
            editQuestion();
        });
        
        $('.button_answer_vote').click(function(evt){
            evt.preventDefault();
            vote(this);
        });
    }
}
