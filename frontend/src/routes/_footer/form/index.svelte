<script>
	export const prerender = true;

	import { template } from './template.js';
	import SVG from '$lib/svg.svelte';

	import Sending from './sending.svelte';

	let form = {};
	let error = {};

	const validate = () => {
		error = {};
		if (!form.name) {
			error.name = 'Please enter your name';
		}

		if (!form.email) {
			error.email = 'Please enter your email address';
		} else if (!/\S+@\S+\.\S+/.test(form.email)) {
			error.email = 'Please enter a valid email address';
		}

		if (!form.msg) {
			error.msg = 'Please enter your message';
		}

		if (Object.keys(error).length === 0) {
			submit();
		}
	};

	let state = 0;
	const submit = async () => {
		state = 1;
		const resp = await fetch('https://formspree.io/f/xknkjbpb', {
			method: 'post',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(form)
		});

		const data = await resp.json();

		if (resp.ok) {
			state = 2;
		} else {
			state = 0;
			error.form = data.error;
		}
	};

	let msgStore = '';
</script>

<div class="form_position">
	{#if state > 0}
		<Sending
			{state}
			on:closed={() => {
				state = 0;
				form = {};
			}}
		/>
	{/if}

	<form on:submit|preventDefault={validate}>
		<div class="inputGroup">
			<label for="name">Full Name</label>
			<input placeholder="Your Name" type="text" id="name" bind:value={form.name} />
			<div class="svg">
				<SVG type="username" size="25" />
			</div>
			{#if error.name}
				<p class="err">
					{error.name}
				</p>
			{/if}
		</div>
		<div class="inputGroup">
			<label for="email">Email Address</label>
			<input placeholder="Your Email Address" type="text" id="email" bind:value={form.email} />
			<div class="svg">
				<SVG type="emailAddress" size="25" />
			</div>
			{#if error.email}
				<p class="err">
					{error.email}
				</p>
			{/if}
		</div>
		<div class="inputGroup">
			<select name="template" id="" bind:value={form.msg}>
				<option value={msgStore}>Message</option>
				{#each template as temp}
					<option value={temp.text}>{temp.name}</option>
				{/each}
			</select>

			<textarea
				placeholder="Your Message"
				id="message"
				bind:value={form.msg}
				on:input={() => (msgStore = form.msg)}
			/>
			{#if error.msg}
				<p class="err">
					{error.msg}
				</p>
			{/if}
		</div>
		{#if error.form}
			<p class="err">
				{error.form}
			</p>
		{/if}
		<div class="inputGroup">
			<input type="submit" value="Send Message" />
		</div>
	</form>
</div>

<style>
	* {
		font-family: var(--font1);
	}

	.form_position {
		position: relative;
	}
	.inputGroup {
		--inputHeight: 40px;

		position: relative;
	}
	.inputGroup:not(:last-child) {
		margin-bottom: 20px;
	}
	label {
		display: inline-block;
		margin-bottom: 10px;
		color: var(--color1);
	}

	input,
	textarea {
		width: 100%;
		height: var(--inputHeight);

		border-radius: calc(var(--inputHeight) / 2);
		border: 2px solid var(--colorNill);

		padding: 10px;

		font-size: 1rem;

		background-color: var(--color6);

		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	[type='text'] {
		padding-left: var(--inputHeight);
	}
	textarea {
		display: block;
		resize: none;
		height: 150px;
	}
	[type='submit'] {
		color: var(--color1);
		background-color: transparent;
		border-color: var(--color1);
	}
	.svg {
		--svgSize: 25px;

		position: absolute;

		top: 34px;
		left: calc((var(--inputHeight) - var(--svgSize)) / 2);

		fill: var(--color2);

		transition: all var(--animTime1);
		transition-timing-function: ease-in-out;
	}
	select {
		color: var(--color1);
		background-color: transparent;
		font-size: 16px;
		border: none;
		margin-bottom: 10px;
	}
	option {
		color: var(--color2);
	}

	input:focus,
	textarea:focus {
		/* outline: none;  */
		background-color: var(--color1);
		border-color: var(--color3);
	}

	[type='submit']:hover,
	[type='submit']:focus {
		background-color: var(--color3);
		border-color: transparent;
	}

	[type='text']:hover + .svg,
	[type='text']:focus + .svg,
	.svg:hover {
		fill: var(--color3);
	}

	.err {
		margin: 0;
		margin-top: 5px;
		color: var(--fColor3);
	}
</style>
