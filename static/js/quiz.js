var data = JSON.parse("{{ data|escapejs }}");
        let ques = data.questions;
        let opt = data.options;
        let answer = data.answers;
        
     
        let length_of_q = ques.length;
        
        let score = 0
        
        curr_ques = 0
        let option_a = document.getElementById("option-a");
        let option_b = document.getElementById("option-b");
        let option_d = document.getElementById("option-d");
        let option_c = document.getElementById("option-c");
        let question = document.getElementById("question");
        
        question.textContent = ques[curr_ques];
        option_a.innerHTML = opt[curr_ques][0];
        option_b.innerHTML = opt[curr_ques][1];
        option_c.innerHTML = opt[curr_ques][2];
        option_d.innerHTML = opt[curr_ques][3];
        
        function updateQuestion(){
            question.textContent = ques[curr_ques];
            option_a.innerHTML = opt[curr_ques][0];
            option_b.innerHTML = opt[curr_ques][1];
            option_c.innerHTML = opt[curr_ques][2];
            option_d.innerHTML = opt[curr_ques][3];
        }
        
        function choice(element){
        
            if(element.innerText===answer[curr_ques]){
         
                score+=1
                console.log("correct answer");
            }
            else{
                
                console.log("incorrect answer");
            }
        
            curr_ques+=1
            if(length_of_q!==curr_ques){
            updateQuestion();
            }
            else{
                tag = "<span class='result'>your score is " + score + "</span>"
                document.getElementById('options').innerHTML = tag;
                document.getElementById('question').innerHTML = "";
               
                $.ajax({
                    type: "POST",
                    url: "/updated_score/",
                    data: {
                       'updated_data': score,
                       csrfmiddlewaretoken: '{{ csrf_token }}'
                    },
                    success: function(response) {
                       console.log(response);
                    },
                    error: function(error) {
                       console.log(error);
                    }
                 });
                 
        
            }
        }