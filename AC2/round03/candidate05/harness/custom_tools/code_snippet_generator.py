def run(ctx, args):
    family = args.get("family", "steps")
    n_variants = args.get("n_variants", 5)
    snippets = []
    for i in range(n_variants):
        if family == "steps":
            var_code = """def _create_initializer(self, key, pattern_idx):
n = self.hypers.num_intervals
f = jnp.zeros(n)
if pattern_idx == 0:
    f = f.at[int(0.15*n):int(0.35*n)].set(1.0)
    f = f.at[int(0.35*n):int(0.55*n)].set(2.0)
    f = f.at[int(0.55*n):int(0.75*n)].set(1.5)
    f = f.at[int(0.75*n):int(0.95*n)].set(0.8)
elif pattern_idx == 1:
    f = f.at[int(0.1*n):int(0.3*n)].set(1.2)
    f = f.at[int(0.3*n):int(0.5*n)].set(2.5)
    f = f.at[int(0.5*n):int(0.7*n)].set(1.3)
    f = f.at[int(0.7*n):int(0.9*n)].set(0.9)
return f"""
            snippets.append(("steps_" + str(i), var_code))
        elif family == "gaussian":
            K_val = 3 if i < 3 else 5
            sigma_base = 0.07
            var_code = """def _create_initializer(self, key, pattern_idx):
n = self.hypers.num_intervals
K = {K_val}
means = jnp.linspace(0.1, 0.9, K)
sigmas = jnp.ones(K) * ({sigma_base + i * 0.02})
f = jnp.zeros(n)
for k in range(K):
    gaussian = jnp.exp(-0.5 * ((jnp.arange(n) - means[k] * n) / sigmas[k])**2)
    f = f + 0.5 * gaussian
return f""".format(K_val=K_val, sigma_base=sigma_base)
            snippets.append(("gaussian_" + str(i), var_code))
        elif family == "exponential":
            rates_list = [0.5, 1.0, 2.0] if i < 3 else [0.3, 0.8, 1.5, 2.5, 3.0]
            rates_str = str(rates_list)
            var_code = """def _create_initializer(self, key, pattern_idx):
n = self.hypers.num_intervals
K = {K_val}
rates = jnp.array({rates_str})
f = jnp.zeros(n)
for rate in rates[:K]:
    exponential = jnp.exp(-rate * (jnp.arange(n) - 0.5 * n))
    f = f + 0.3 * exponential
return f""".format(K_val=i+1, rates_str=rates_str)
            snippets.append(("exponential_" + str(i), var_code))
    return {"snippets": snippets, "family": family, "n_variants": n_variants}
