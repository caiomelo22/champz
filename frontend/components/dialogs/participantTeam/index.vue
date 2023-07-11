<template>
  <v-card>
    <v-card-title>
      <h5>{{ currentParticipant.name }}'s Team</h5>
    </v-card-title>
    <v-card-text>
      <div class="champz-table-wrapper">
        <table class="champz-table">
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Name</th>
              <th scope="col">Overall</th>
              <th scope="col">Price</th>
              <th scope="col" class="text-center">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(player, i) in selectedTeam" :key="i">
              <th scope="row">{{ player.id }}</th>
              <td>{{ player.name }}</td>
              <td>{{ player.overall }}</td>
              <td>{{ player.value }}</td>
              <td class="text-center">
                <v-btn color="red" small dark @click="$emit('remove', player)">
                  Remove Buy
                </v-btn>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </v-card-text>
  </v-card>
</template>
<script src="./index"></script>