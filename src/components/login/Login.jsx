import React, { useState, useCallback } from 'react';
import './login.css';

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errors, setErrors] = useState({});
    const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+$/;

    const validateForm = useCallback(() => {
        const newErrors = {};
        if (!email) {
        newErrors.email = 'O campo e-mail é obrigatório.';
        } else if (!emailRegex.test(email)) {
        newErrors.email = 'O formato do e-mail é inválido.';
        };

        if (!password) {
        newErrors.password = 'O campo senha é obrigatório.';
        }else if (password.length < 8) {
            newErrors.password = 'A senha deve ter no mínimo 8 caracteres.';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    }, [email, password, emailRegex]);

    const handleSubmit = useCallback((event) => {
        event.preventDefault();
        if (validateForm()) {
            console.log('Formulário válido!');
            alert(`Login simulado com sucesso!\nE-mail: ${email}`);
        } else {
            console.log('Formulário inválido.');
        }
    }, [validateForm, email]);

    return (
        <div className="login-container">
            <form className="login-form" onSubmit={handleSubmit} noValidate> 
                <img src="./public/real-time.png" width="10%" height="10%" /><h2>Login</h2>

                <p>Acesse a plataforma</p>

                <div className="input-group">
                    <label htmlFor="email">E-mail</label>
                    <input
                        type="email"
                        id="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="seu@email.com"
                        className={errors.email ? 'input-error' : ''}
                        aria-invalid={errors.email ? "true" : "false"}
                    />
                    {errors.email && <span className="error-message">{errors.email}</span>}
                </div>

                <div className="input-group">
                    <label htmlFor="password">Senha</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Sua senha"
                        className={errors.password ? 'input-error' : ''}
                        aria-invalid={errors.password ? "true" : "false"}
                    />
                    {errors.password && <span className="error-message">{errors.password}</span>}
                </div>

                <button type="submit" className="login-button">Entrar</button>
            </form>
        </div>
    );
};

export default Login;