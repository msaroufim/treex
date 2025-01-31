import jax
import jax.numpy as jnp
import numpy as np
import optax

import treex as tx


class TestOptreex:
    def test_apply_updates(self):

        optax_optim = optax.adam(0.1)
        optimizer = tx.Optimizer(optax_optim)

        linear = tx.Linear(2, 3).init(42)
        optimizer = optimizer.init(linear)
        opt_state = optax_optim.init(linear)

        @jax.grad
        def loss_fn(linear: tx.Linear):
            return sum(
                jax.tree_leaves(jax.tree_map(lambda x: jnp.mean(x ** 2), linear)), 0.0
            )

        grads = loss_fn(linear)

        optax_params: tx.Linear
        optax_updates, opt_state = optax_optim.update(grads, opt_state, linear)
        optax_params = optax.apply_updates(optax_updates, linear)
        treex_params = optimizer.apply_updates(grads, linear)

        assert all(
            np.allclose(a, b)
            for a, b in zip(jax.tree_leaves(opt_state), jax.tree_leaves(optimizer))
        )
        assert all(
            np.allclose(a, b)
            for a, b in zip(
                jax.tree_leaves(optax_params), jax.tree_leaves(treex_params)
            )
        )

    def test_return_updates(self):

        optax_optim = optax.adam(0.1)
        optimizer = tx.Optimizer(optax_optim)

        linear = tx.Linear(2, 3).init(42)
        optimizer = optimizer.init(linear)
        opt_state = optax_optim.init(linear)

        @jax.grad
        def loss_fn(linear: tx.Linear):
            return sum(
                jax.tree_leaves(jax.tree_map(lambda x: jnp.mean(x ** 2), linear)), 0.0
            )

        grads = loss_fn(linear)

        optax_updates: tx.Linear
        optax_updates, opt_state = optax_optim.update(grads, opt_state, linear)
        treex_updates = optimizer.apply_updates(grads, linear, return_updates=True)

        assert all(
            np.allclose(a, b)
            for a, b in zip(jax.tree_leaves(opt_state), jax.tree_leaves(optimizer))
        )
        assert all(
            np.allclose(a, b)
            for a, b in zip(
                jax.tree_leaves(optax_updates), jax.tree_leaves(treex_updates)
            )
        )
