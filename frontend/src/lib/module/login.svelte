<script>
	// import { goto } from '$app/navigation';
	import { api_url, _user, module } from '$lib/store.js';
	import { token } from '$lib/cookie.js';

	import Input from '$lib/comp/input_group.svelte';
	import Button from '$lib/comp/button.svelte';

	let form = {};
	let error = {};

	const validate = () => {
		error = {};
		if (!form.email) {
			error.email = 'cannot be empty';
		}
		if (!form.password) {
			error.password = 'cannot be empty';
		}

		Object.keys(error).length === 0 && submit();
	};

	const submit = async () => {
		const resp = await fetch(`${api_url}/login`, {
			method: 'post',
			headers: {
				'Content-Type': 'application/json',
				Authorization: $token
			},
			body: JSON.stringify(form)
		});

		if (resp.ok) {
			const data = await resp.json();
			if (data.status == 200) {
				// $module = '';
				// $_user = data.data.user;
				$token = data.data.token;

				document.location = '/';
			
			} else {
				error.form = data.message;
			}
		}
	};
</script>

<section>
	<strong class="big"> Login </strong>
	<form on:submit|preventDefault novalidate autocomplete="off">
		{#if error.form}
			<p class="error">
				{error.form}
			</p>
		{/if}
		<Input name="email" error={error.email} let:id>
			<input placeholder="email here" type="text" {id} bind:value={form.email} />
		</Input>
		<Input name="password" error={error.password} let:id>
			<input placeholder="password here" type="password" {id} bind:value={form.password} />
		</Input>

		<Button
			on:click={() => {
				validate();
			}}
		>
			Submit
		</Button>
	</form>
</section>

<style>
	section {
		display: flex;
		flex-direction: column;

		width: 100%;
	}
	strong,
	form {
		padding: var(--gap3);
	}
	strong {
		border-bottom: 2px solid var(--mid_color);
	}
</style>
