function [a,b] = SeparatingHyperplane(p, labels)
   %p should have the size of (# of equations, # of dimensions)
   %labels should have the size of (# of equations)
   size_of_p = size(p);
   num_of_equations = size_of_p(1);
   num_of_variables = size_of_p(2);
   size_of_labels = size(labels);
   
   if size_of_p(1)~=size_of_labels(1)
       fprintf('Size does not match, please check!\n');
       return;
   end
   c = [zeros(num_of_variables,1); 0; ones(num_of_equations,1)];
   c_norm = [ones(num_of_variables,1); 0; zeros(num_of_equations,1)];
   b = [-1*ones(num_of_equations,1);zeros(num_of_equations,1)];
   svT = [];
   for i =1:num_of_equations
       svT = [svT;-labels(i)*p(i,:)];
   end
   constraint_matrix = [svT ,-labels, -1*eye(num_of_equations);zeros(num_of_equations,num_of_variables+1),-1*eye(num_of_equations)];
   cvx_begin
   variables u(num_of_variables+num_of_equations+1, 1)
   minimize(c'*u+norm(c_norm.*u, 2))
   subject to
   constraint_matrix*u<=b
   cvx_end
   
   a = u(1:num_of_variables);
   b = u(1+num_of_variables);
   
end